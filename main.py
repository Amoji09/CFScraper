from bs4 import BeautifulSoup
from scrapingant_client import ScrapingAntClient

# Define URL with a dynamic web content
url = "https://app.careerfairplus.com/gt_ga/fair/3990"

# Create a ScrapingAntClient instance
client = ScrapingAntClient(token='57278df6b3e94ab189cf9cf2d8169947')

# Get the HTML page rendered content
page_content = client.general_request(url).content

# Parse content with BeautifulSoup
soup = BeautifulSoup(page_content, "html.parser")
#print(soup.prettify())

containers = soup.find_all("div", class_ = "employer-list-item-container")
companies = []
company_names = []
for container in containers:
    companies.append(container.find("span", class_ = "MuiTypography-root MuiListItemText-primary MuiTypography-body1 MuiTypography-displayBlock"))
for company in companies:
    company_names.append(company.text)
    
levels = "https://www.levels.fyi/internships/"
page_content = client.general_request(levels).content
soup = BeautifulSoup(page_content, "html.parser")


level_rows = soup.findAll("tr")


level_comps = {}
for comp in level_rows:
    compName = comp.find(class_ = "font-weight-bold mt-1 mb-2 mx-auto")
    
    try:
        compSalary = comp.find(class_ = "salary-info").find("h6")
        name = compName.text.strip()
        salary = compSalary.text.strip("hr").strip(" /").strip("$")
        level_comps[name] = int(salary)
    except AttributeError:
        print("", end = "")


present_comps = []

for name in range(len(company_names)):
    salary = level_comps.get(company_names[name])
    if salary != None:
        present_comps.append([company_names[name],salary])

present_comps = sorted(present_comps,key=lambda x : x[1], reverse=True)

f = open("output.txt", "a")
f.truncate(0)
for company in present_comps:
    out = company[0] + " : " + str(company[1]) + "\n"
    f.write(out);

f.close()