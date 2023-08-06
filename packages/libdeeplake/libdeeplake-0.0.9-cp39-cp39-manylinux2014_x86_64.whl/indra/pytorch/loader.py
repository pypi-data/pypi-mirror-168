from itertools import repeat
from typing import Callable, List, Optional
from indra.pytorch.buffered_loader import BufferedLoader
from indra.pytorch.util import get_indexes, transform_collate_batch
from indra.pytorch.common import collate_fn as default_collate
import multiprocessing as mp
from pathos.pools import ProcessPool
from hub.integrations.pytorch.shuffle_buffer import ShuffleBuffer

try:
    import torch

    torch.set_num_threads(1)
except ImportError:
    pass

MB = 1024 * 1024

class Loader:
    def __init__(
        self,
        dataset,
        batch_size: Optional[int] = 1,
        shuffle: bool = False,
        drop_last: bool = False,
        return_index: bool = True,
        transform_fn: Optional[Callable] = None,
        num_workers: int = 0,
        num_threads: Optional[int] = None,
        collate_fn: Optional[Callable] = default_collate,
        distributed=False,
        tensors: Optional[List[str]] = None,
        raw_tensors: Optional[List[str]] = None,
        prefetch_factor: int = 10,
        upcast: bool = True,
        primary_tensor: Optional[str] = None,
        buffer_size: int = 2048,
    ):
        """Returns a Loader object referencing to C++ dataloader instance.

        Args:
            batch_size (int, optional): how many samples per batch to load
                (default: ``1``).
            shuffle (bool, optional): set to ``True`` to have the data reshuffled at every epoch
                (default: ``False``).
            drop_last (bool, optional): set to ``True`` to drop the last incomplete batch,
                if the dataset size is not divisible by the batch size. If ``False`` and
                the size of dataset is not divisible by the batch size, then the last batch
                will be smaller. (default: ``False``)
            retrun_index (nool) Showing wheter Loader needs to return the sample index during iteration.Defaults to True.
            num_workers (int, optional): how many subprocesses to use for data
                loading. ``0`` means that the data will be loaded in the main process.
                (default: ``0``)
            num_threads (int, optional) number of threads that nedes to be spinned up during data loading. Defaults to None.
                if it is none then we are detecting the hardware concurency count to set.
                Note: We don't set any threading flags (eg. OMP_NUM_THREADS, MKL_NUM_THREADS, etc)
                to get more performant Loader consider of not setting those flags which can affect on 3rd party libraries worflow performance
            transform_fn (Callable, optional) Callable object which is needed to be applyed on each sample on batch. Defaults to None.
            collate_fn (callable, optional): merges a list of samples to form a
                mini-batch of Tensor(s).  Used when using batched loading from a
                map-style dataset.
            distributed (nool) flag that is showing wheter Loader needes to work in DDP or not. Defaults to ``False``
            tensors (List[str], optinal) List of tensors thet are participating to in Loadeing process.
                Defaults to ``None`` which means that Loader will fetch samples for all of the tensors
            raw_tensors (List[str], optional) List of the tensors that needs to return raw data instead of decompression.
                Defaults to ``None`` if raw_tensors is None then all the tensors will send decompression data
                E.g raw_tensors['images'] then only the images tensor data will be sent as a row array
            prefetch_factor (int) Number of samples loaded in advance by workers. Defaults to 10
            upcast (bool) floag that is showing wheter we need to upcast object if dtype is not supported this is needed only for
                pytoarch as it is not support all the dtypes. Defaults to True.
            buffer_size (int): The size of the buffer used to shuffle the data in MBs. Defaults to 2048 MB. Increasing the buffer_size will increase the extent of shuffling.
        """
        if primary_tensor is not None:
            dataset.primary_tensor = primary_tensor
        if num_workers < 0:
            raise ValueError("num_workers must be non-negative")
        if num_threads is not None and num_threads <= 0:
            raise ValueError("num_threads must be positive")
        tensors = tensors or []
        raw_tensors = raw_tensors or []
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.drop_last = drop_last
        self.return_index = return_index
        self.transform_fn = transform_fn
        self.num_workers = num_workers
        self.num_threads = num_threads
        self.collate_fn = collate_fn
        self.distributed = distributed
        self.tensors = tensors
        self.raw_tensors = raw_tensors
        self.prefetch_factor = prefetch_factor
        self.upcast = upcast
        self.pool = None
        self._dataloader = None
        self.buffer = ShuffleBuffer(buffer_size * MB) if self.shuffle else None


    def start_processes(self):
        if self.pool is not None:
            return
        self.pool = ProcessPool(nodes=self.num_workers)
        m = mp.Manager()
        self.data_in_queues = [m.Queue() for _ in range(self.num_workers)]
        self.data_out_queues = [m.Queue() for _ in range(self.num_workers)]

    def run_workers(self):
        inp = list(
            zip(
                self.data_in_queues,
                self.data_out_queues,
                repeat(self.transform_fn),
                repeat(self.collate_fn),
                repeat(self.upcast),
            )
        )
        self.pool.amap(early_transform_collate, inp)

    def __iter__(self):
        if self._dataloader is None:
            dataset = self.dataset
            if self.distributed:
                indexes = get_indexes(dataset, shuffle=self.shuffle)
                dataset = dataset[indexes]

            self._dataloader = create_dataloader(
                dataset=dataset,
                drop_last=self.drop_last,
                return_index=self.return_index,
                batch_size=self.batch_size,
                num_threads=self.num_threads,
                tensors=self.tensors,
                raw_tensors=self.raw_tensors,
                shuffle=False,
            )

        if self.num_workers == 0:
            yield from self.zero_worker_iter()
        else:
            yield from self.multiprocess_iter()

    @property
    def dataloader(self):
        return BufferedLoader(self._dataloader, self.buffer, self.batch_size, self.drop_last) if self.shuffle else self._dataloader

    def zero_worker_iter(self):
        for batch in self.dataloader:
            yield transform_collate_batch(
                batch, self.transform_fn, self.collate_fn, self.upcast
            )

    def multiprocess_iter(self):
        self.start_processes()
        self.run_workers()
        num_prefetch_tasks = self.prefetch_factor * self.num_workers
        dataloader = self.dataloader
        i = 0
        while 1:
            wid = i % self.num_workers
            if i >= num_prefetch_tasks:
                out = self.data_out_queues[wid].get()
                if out is None:
                    # get None from other workers too, to empty the queues
                    for j in range(self.num_workers):
                        if j != wid:
                            self.data_out_queues[j].get()
                    break
                if isinstance(out, Exception):
                    raise out

            if i < len(dataloader):
                batch = next(dataloader)
                self.data_in_queues[wid].put(batch)
            elif i == len(dataloader):
                try:
                    next(dataloader)
                except StopIteration:
                    pass
                # send None (stop signal) to all workers
                for j in range(self.num_workers):
                    self.data_in_queues[j].put(None)
            if i >= num_prefetch_tasks:
                yield out
            i += 1


def create_dataloader(
    dataset,
    batch_size,
    num_threads,
    tensors,
    raw_tensors,
    drop_last=False,
    shuffle=False,
    return_index=True,
):
    if num_threads is None:
        return dataset.loader(
            batch_size=batch_size,
            tensors=tensors,
            raw_tensors=raw_tensors,
            drop_last=drop_last,
            shuffle=shuffle,
            return_index=return_index,
        )

    return dataset.loader(
        batch_size=batch_size,
        num_threads=num_threads,
        tensors=tensors,
        raw_tensors=raw_tensors,
        drop_last=drop_last,
        shuffle=shuffle,
        return_index=return_index,
    )


def early_transform_collate(inp):
    data_in_queue, data_out_queue, transform_fn, collate_fn, upcast = inp
    while 1:
        batch = data_in_queue.get()
        if batch is None:
            data_out_queue.put(None)
            break
        try:
            out = transform_collate_batch(batch, transform_fn, collate_fn, upcast)
            data_out_queue.put(out)
        except Exception as e:
            data_out_queue.put(e)
            break
