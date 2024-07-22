from ranx import Qrels, Run
"""
This code provides functions for creating and evaluating
document ranking systems using the ranx library
"""

def create_ubuntu_qrels():
    pass

def create_qrels(index_data,column_name):
    """
    This function creates a Qrels object from the index_data DataFrame.
    It iterates over the unique queries in the index_data DataFrame.
    For each query, it creates a dictionary mapping document IDs to their corresponding ratings.
    The function returns a Qrels object containing the query-document relevance scores.
    """
    qrels_dict = {}
    # index_data = search_data_index_hot
    queries = index_data['query name'].unique()
    
    for i in range(len(queries)):
        current_queries = queries[i]
        query_dict = {}
        current_index = index_data[index_data['query name']==current_queries]
        for doc_idx,rating in zip(current_index.index,current_index[column_name]):
            query_dict[str(doc_idx)] = rating
        qrels_dict[str(i)] = query_dict
    return Qrels(qrels_dict)


def create_run(results,index_data):
    """
    This function creates a Run object from the results dictionary and index_data DataFrame.
    It iterates over the unique queries in the index_data DataFrame.
    For each query, it creates a dictionary mapping document IDs to their corresponding scores (calculated as 1 / (distance + 1e-10)).
    The function returns a Run object containing the query-document scores.
    """
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

def evaluate_algs(results,index_data,column_name):
    """
    This function evaluates the performance of an information retrieval system.
    It calls the create_qrels and create_run functions to create the Qrels and Run objects.
    It defines a list of evaluation metrics to be used, including recall, precision, hits, MAP, MRR, and NDCG at ranks 10 and 40.
    The function returns the evaluation results using the evaluate function from ranx.
    """
    qrels = create_qrels(index_data,column_name)
    run = create_run(results,index_data)
    
    metrics = ["recall@10","precision@10","hits@10","map@10", "mrr@10", "ndcg@10"]
    metrics += ["recall@40","precision@40","hits@40","map@40", "mrr@40", "ndcg@40"]
    return evaluate(qrels, run, metrics,make_comparable=True)



def compare_algs(results_list,index_data,column_name):
    metrics = ["recall@10","precision@10","hits@10","map@10", "mrr@10", "ndcg@10"]
    metrics += ["recall@40","precision@40","hits@40","map@40", "mrr@40", "ndcg@40"]
    
    qrels = create_qrels(index_data,column_name)
    runs = [create_run(result,index_data) for result in results_list]
    
    return compare(
    qrels=qrels,
    runs=runs,
    metrics=metrics,
    max_p=0.01,  # P-value threshold
    make_comparable=True
)