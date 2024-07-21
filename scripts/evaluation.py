from ranx import Qrels, Run

def create_qrels(index_data):
    qrels_dict = {}
    index_data = search_data_index_hot
    queries = index_data['query name'].unique()
    
    for i in range(len(queries)):
        current_queries = queries[i]
        query_dict = {}
        current_index = index_data[index_data['query name']==current_queries]
        for doc_idx,rating in zip(current_index.index,current_index.rating_hottest):
            query_dict[str(doc_idx)] = rating
        qrels_dict[str(i)] = query_dict
    return Qrels(qrels_dict)

def create_run(results,index_data):
    runs = {}
    queries = index_data['query name'].unique()
    results
    for i in range(len(queries)):
        
        res_dict = {}
        for doc_idx,rating in zip(results['ids'][i],results['distances'][i]):
            res_dict[str(doc_idx)] = 1/(rating+1e-10)
        runs[str(i)] = res_dict
    return Run(runs)


from ranx import compare, evaluate

def evaluate_algs(results,index_data):
    qrels = create_qrels(index_data)
    run = create_run(results,index_data)
    
    metrics = ["recall@10","precision@10","hits@10","map@10", "mrr@10", "ndcg@10"]
    metrics += ["recall@40","precision@40","hits@40","map@40", "mrr@40", "ndcg@40"]
    return evaluate(qrels, run, metrics,make_comparable=True)

def compare_algs(results_list,index_data):
    metrics = ["recall@10","precision@10","hits@10","map@10", "mrr@10", "ndcg@10"]
    metrics += ["recall@40","precision@40","hits@40","map@40", "mrr@40", "ndcg@40"]
    
    qrels = create_qrels(index_data)
    runs = [create_run(result,index_data) for result in results_list]
    
    return compare(
    qrels=qrels,
    runs=runs,
    metrics=metrics,
    max_p=0.01,  # P-value threshold
    make_comparable=True
)


def store_vectors(embeddings,dataset,file_name):
    embeddings = embeddings.detach()
    EMBEDDING_DATA_PATH
    datasets_to_store = {"path":[],"index":[],"embedding":[]}
    for i,data in dataset_train [['path',"index"]].iterrows():
        datasets_to_store["embedding"].append(embeddings[i].tolist())
        datasets_to_store["path"].append(data['path'])
        datasets_to_store["index"].append(data['index'])

    datasets_to_store = pd.DataFrame(datasets_to_store)
    datasets_to_store.to_json(EMBEDDING_DATA_PATH+"/"+file_name+".json")