def Search(query, page, search):
    keywords = query.split()
    results = search(keywords)
    results = make_pages(results, page)
    return results


def make_pages(dic, page):
  start= (page - 1) * 15
  end = start + 15
  items_lst = list(dic.items())
  items = items_lst[start:end]
  page_dic = dict(items)

  return page_dic

