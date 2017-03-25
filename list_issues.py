import github
import sys
token = open(".github_api_token", 'r').read()

g = github.Github() # login_or_token=token)

pw = g.get_organization("pywren")
repo = pw.get_repo('pywren')


ISSUE_URL_TEMPLATE = "https://github.com/pywren/pywren/issues/{}"

label_dict = {}
for l in repo.get_labels():
    label_dict[l.name] = l.color, l.url

for issue in repo.get_issues(state='closed'):
    if issue.milestone:
        if issue.milestone.title == sys.argv[1]:
            
            label_str = ""
            for l in issue.labels:
                label_name = l.name
                label_color, label_url = label_dict[label_name]
                label_str += '<span class="label label-default">{}</span>'.format(label_name)
            print "* [[{}]({})] {} {}".format(issue.number, 
                                           ISSUE_URL_TEMPLATE.format(issue.number), 
                                           issue.title, label_str)
            


    #if issue.milestone == 'closed':
    #    print issue.closed_at

