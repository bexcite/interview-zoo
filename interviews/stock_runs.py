def stock_runs(prices):
    max_run = float('-inf')
    pos_run = 1
    neg_run = 1

    prev_price = prices[0]
    for price in prices[1:]:
        if price < prev_price:
            neg_run += 1
            max_run = max(max_run, pos_run)
            pos_run = 1
        else:
            pos_run += 1
            max_run = max(max_run, neg_run)
            neg_run = 1
        prev_price = price

    return max(max_run, neg_run, pos_run)


stock_runs([1, 2, 3])
