from operator import contains
from bs4 import BeautifulSoup
from scrapingant_client import ScrapingAntClient

# Define URL with a dynamic web content
url = "https://github.com/pittcsc/Summer2023-Internships"

# Create a ScrapingAntClient instance
token = ""

with open("token.txt") as f:
    token = f.readline().rstrip()


client = ScrapingAntClient(token=token)

# Get the HTML page rendered content
page_content = client.general_request(url).content

# Parse content with BeautifulSoup
soup = BeautifulSoup(page_content, "html.parser")
# print(soup.prettify())

table_rows = soup.findChildren('tbody')
company_names = []
for i in range(len(table_rows)):
    links = table_rows[i].findChildren('a')
    for link in links:
        company_names.append(link.text)

levels = "https://www.levels.fyi/internships/"
page_content = client.general_request(levels).content
soup = BeautifulSoup(page_content, "html.parser")


level_rows = soup.findAll("tr")


level_comps = {}
for comp in level_rows:
    compName = comp.find(class_="font-weight-bold mt-1 mb-2 mx-auto")

    try:
        compSalary = comp.find(class_="salary-info").find("h6")
        name = compName.text.strip()
        salary = compSalary.text.strip("hr").strip(" /").strip("$")
        level_comps[name] = float(salary)
    except AttributeError:
        print("", end="")


present_comps = []
non_present = []
for name in range(len(company_names)):
    tempName = ""

    salary = level_comps.get(company_names[name])
    if salary != None:
        present_comps.append([company_names[name], salary])
    else:
        found = False
        for key in level_comps.keys():
            if key in company_names[name]:
                tempName = key
                salary = level_comps.get(key)
                present_comps.append([company_names[name], salary])
                found = True
                break
        if not found:
            non_present.append(company_names[name])


present_comps = sorted(present_comps, key=lambda x: x[1], reverse=True)

f = open("output.txt", "a")
f.truncate(0)
for company in present_comps:
    out = company[0] + " : " + str(company[1]) + "\n"
    f.write(out)
f.write("Not Found:\n")
for company in non_present:
    out = company + "\n"
    f.write(out)

f.close()
