from bs4 import BeautifulSoup
import requests
import re

run_script = True
num_pages = 4
while run_script:
#-----------------------------------------------------------MicroCenter-------------------------------------------------------------------------------------------------
    original_search_term = str(input("--------------------------------------------------------------------------- \nWelcome to the Computer Part Price Checker! \nWhat product do you want to search for (Include a number to specify your search such as 750W power supply or 3.5ghz CPU): "))
    search_term = "".join([w.replace(' ', '+') for w in original_search_term])
    url = f"https://www.microcenter.com/search/search_results.aspx?Ntt={search_term}&Ntx=mode+MatchPartial&Ntk=all&sortby=match&N=4294966998&myStore=true&page=1"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    page_text = doc.find(class_="pages inline")
    items_found = {}
    items = []

    if page_text!=None:
        page_text = page_text.find_all('a')
        pages = 1
        if len(page_text)>1:
            pages = int(page_text[-2].string)

        criteria = re.findall(r'\d+', original_search_term)
        criteria = [int(x) for x in criteria]

        for page in range(1, min(num_pages,pages+1)):
            url = f"https://www.microcenter.com/search/search_results.aspx?Ntt={search_term}&Ntx=mode+MatchPartial&Ntk=all&sortby=match&N=4294966998&myStore=true&page={page}"
            page = requests.get(url).text
            doc = BeautifulSoup(page, "html.parser")
            divs = doc.find(class_ = "products col3")
            divs = divs.find_all('a')

            for div in divs:
                if len(criteria)!=0:
                    items += div.find_all(text=re.compile(str(max(criteria))))
                else:
                    items += div.find_all(text=re.compile(original_search_term))
                    items += div.find_all(text=re.compile(original_search_term.upper()))

            for item in items:
                parent = item.parent
                link = "https://www.microcenter.com/"+parent['href']
                next_parent = item.find_parent(class_="details")
                price_parent = next_parent.find(class_="price")
                price_line = str(price_parent.find_all("span")[-2])
                price = re.findall(r'\d+', price_line)
                if len(price)<=2:
                    price = price[0]
                else:
                    price = ''.join(price[0:-1])
                items_found[item+" @Micro_Center"] = {"price": int(price.replace(",", "")), "link": link}

#--------------------------------------------------------Memory Express-------------------------------------------------------------------------------------------------

    url = f"https://www.memoryexpress.com/Search/Products?Search={search_term}&Page=1"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    page_text = doc.find(class_="AJAX_List_Pager AJAX_List_Pager_Compact")

    if page_text!=None:
        page_text = page_text.find_all('a')
        pages = 1
        if len(page_text) > 1:
            pages = int(page_text[-2].string)

        items = []
        items_prices = []
        items_links = []

        criteria = re.findall(r'\d+', original_search_term)
        criteria = [int(x) for x in criteria]

        for page in range(1, pages+1):
            url = f"https://www.memoryexpress.com/Search/Products?Search={search_term}&Page={page}"
            page = requests.get(url).text
            doc = BeautifulSoup(page, "html.parser")
            divs = doc.find(class_ = "c-shca-container")
            divs = divs.find_all(class_ = "c-shca-icon-item__body-name")

            for div in divs:
                temp = ' '.join(div.a.text.split())
                items.append(temp)

            divs = doc.find(class_ = "c-shca-container")
            divs = divs.find_all(class_ = "c-shca-icon-item__summary-list")

            for div in divs:
                temp = ' '.join(div.span.text.split())[1:]
                temp2=""
                for char in temp:
                    if char==".":
                        break
                    if char==",":
                        continue
                    temp2+=char

                temp2 = int(temp2)
                items_prices.append(temp2)
            

            divs = doc.find(class_ = "c-shca-container")
            divs = divs.find_all(class_ = "c-shca-icon-item__body-image")

            for div in divs:
                temp = "https://www.memoryexpress.com"+div.a['href']
                items_links.append(temp)

        for x in range(len(items)):
            if len(criteria)!=0:
                    if str(max(criteria)) in items[x]:
                        items_found[items[x]+" @Memory_Express"] = {"price": int(items_prices[x]), "link": items_links[x]}
            else:
                items_found[items[x]+" @Memory_Express"] = {"price": int(items_prices[x]), "link": items_links[x]}

#--------------------------------Newegg-------------------------------------------------------------------------------------------------------

    url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    page_text = doc.find(class_="list-tool-pagination-text")
    items = []

    if page_text!=None:
        page_text = page_text.strong
        pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

        criteria = re.findall(r'\d+', original_search_term)
        criteria = [int(x) for x in criteria]
            
        for page in range(1, min(num_pages,pages+1)):
            url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131&page={page}"
            page = requests.get(url).text
            doc = BeautifulSoup(page, "html.parser")
            divs = doc.find_all(class_ = "item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")

            for div in divs:
                if len(criteria)!=0:
                    items += div.find_all(text=re.compile(str(max(criteria))))
                else:
                    items += div.find_all(text=re.compile(original_search_term))
                    items += div.find_all(text=re.compile(original_search_term.upper()))

            for item in items:
                parent = item.parent
                if parent.name != 'a':
                    continue
                link = parent['href']
                next_parent = item.find_parent(class_="item-container")
                price = next_parent.find(class_="price-current").strong
                if price == None:
                    continue
                price = price.string
                if item not in items_found:
                    items_found[item+" @Newegg"] = {"price": int(price.replace(",", "")), "link": link}
                else:
                    if items_found[item+" @Newegg"]["price"] > int(price.replace(",", "")):
                        items_found[item+" @Newegg"] = {"price": int(price.replace(",", "")), "link": link}
#---------------------------------------------------------------------------------------------------------------------------------------------

    sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])
    print("Total Results: " + str(len(sorted_items)))

    show_results = True
    first=0
    last = 10
    while show_results:
        copy_sorted = sorted_items
        if len(sorted_items)>10:
            copy_sorted = sorted_items[first:last]
            if last>10:
                print("Displaying the next top 10 cheapest products.")
            else:
                print("Displaying the top 10 cheapest products.")
        else:
            print(f"Displaying the top {len(copy_sorted)} cheapest products.")

        count = 1+first
        for item in copy_sorted:
            print()
            print(str(count)+". "+item[0])
            print(f"${item[1]['price']}")
            print(item[1]['link'])
            print()
            print("----------------------------------------------")    
            count+=1

        if last>=len(sorted_items):
            print("DIsplayed all results. \n")
            show_results=False

        tester = True
        while tester and last<len(sorted_items):
            output = str(input("Would you like to see more results? (y/n): "))
            if output == "y":
                tester=False
                first = last
                last+=10
            elif output == "n":
                tester=False
                show_results=False
            else:
                print("Please enter y or n \n")
        
    invalid = True
    while invalid:
        output = str(input("Would you like to search for another product? (y/n): "))
        if output == "y":
            invalid=False

        elif output == "n":
            print("Thank you for using the Computer Part Price Checker.")
            invalid=False
            run_script=False
        else:
            print("Please enter y or n \n")

