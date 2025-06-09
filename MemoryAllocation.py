
def first_fit(blocks, processes):
    
    allocation = [-1] * len(processes)
    for i, p in enumerate(processes):
        for j, b in enumerate(blocks):
            if b >= p:
                allocation[i] = j
                blocks[j] -= p
                break
    return allocation


def best_fit(blocks, processes):
    
    allocation = [-1] * len(processes)
    for i, p in enumerate(processes):
        best_idx = -1
        for j, b in enumerate(blocks):
            if b >= p:
                if best_idx == -1 or blocks[j] < blocks[best_idx]:
                    best_idx = j
        if best_idx != -1:
            allocation[i] = best_idx
            blocks[best_idx] -= p
    return allocation


def worst_fit(blocks, processes):
    
    allocation = [-1] * len(processes)
    for i, p in enumerate(processes):
        worst_idx = -1
        for j, b in enumerate(blocks):
            if b >= p:
                if worst_idx == -1 or blocks[j] > blocks[worst_idx]:
                    worst_idx = j
        if worst_idx != -1:
            allocation[i] = worst_idx
            blocks[worst_idx] -= p
    return allocation


def paging(process_sizes, page_size):
    
    result = []
    for size in process_sizes:
        pages = size // page_size
        if size % page_size:
            pages += 1
        # fragmentation = leftover in last page
        fragmentation = pages * page_size - size
        result.append({
            'process_size': size,
            'pages_required': pages,
            'internal_fragmentation': fragmentation
        })
    return result