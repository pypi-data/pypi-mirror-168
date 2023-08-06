from indra import api
from .constants import COCO_DS_NAME, MNIST_DS_NAME, IMAGENET_DS_NAME, LAION_400_M_DS_NAME

from time import time

queries = {
    COCO_DS_NAME: [
        ("SELECT * WHERE categories[0] == 'person'", 22706),
        ("SELECT * WHERE shape(categories)[0] == 0", 1021),
        ("SELECT * WHERE shape(boxes)[0] == 5", 7712),
        ("SELECT * WHERE ALL_STRICT(categories == 'person') or shape(categories)[0] == 0", 1375),
        ("SELECT * WHERE ALL(categories == 'person')", 1375),
        ("select * where ALL_STRICT(categories == 'person')", 354),
        ("select * where ALL_STRICT(\"pose/categories\" == 'person')", 64115),
        ("select * where any(categories == 'banana')", 2243),
        ("select * where any(categories == 'person')", 64115),
        ("select * where all_strict(logical_and(categories == 'car', boxes[:,3] > 200))", 5),
        ("select * where any(logical_and(categories == 'car', boxes[:,3] > 200))", 1242),
        ("select * where all_strict(logical_or(categories == 'person', categories == 'banana'))", 873),
        ("select * where logical_and(categories == 'person', categories == 'person')", 208),
        ("SELECT * where images_meta['license'] == 3", 32184),
        ("SELECT * where images_meta['id'] > 285529", 60365),
        ("SELECT * order by images_meta['license']", 118287),
    ],
    MNIST_DS_NAME: [
        ("SELECT * WHERE labels == 0", 5923),
        ("SELECT * WHERE SHAPE(images)[0] == 28", 60000),
        ("SELECT * WHERE SHAPE(images)[0] == 29", 0),
    ],
    IMAGENET_DS_NAME: [
        ("SELECT * WHERE labels == 'bikini'", 1300),
        ("SELECT * WHERE SHAPE(boxes)[0] > 15", 2),
        ("(SELECT * WHERE labels == 'bikini' LIMIT 10) UNION (SELECT * WHERE labels == 1 LIMIT 10) UNION (SELECT * WHERE labels == 43 LIMIT 10)", 30),
    ],
    #LAION_400_M_DS_NAME: [
    #    ("SELECT * WHERE CONTAINS(caption, 'blue')", 2783),
    #    ("SELECT * WHERE caption[0] == 'A'", 28904),
    #    ("SELECT * WHERE SHAPE(image)[0] == 256", 512993),
    #],
    "hub://davitbun/places365-train-challenge": [
        ("SELECT * WHERE labels == 'hotel_room'", 32947),
        ("SELECT * ORDER by random()", 8026628),
    ]
}

def test_dataset_query_results():
    global queries
    for ds_name in queries:
        ds = api.dataset(ds_name)
        for (query, result_size) in queries[ds_name]:
            print(f"\tRunning query: {query}")
            start = time()
            result = ds.query(query)
            print('\tQuery time: ', time() - start)
            assert(len(result) == result_size)
            start = time()
            result = ds.query(query)
            print('\tSecond Query time: ', time() - start)