

def find_suggestions(info):
    context = {}
    sec_not_present= []
    #sections count
    if info['contactNumber'] == None:
        sec_not_present.append("contact")
    if info['linkedIn'] == None:
        sec_not_present.append("linkedIn")
    if len(info['skills'])==0:
        sec_not_present.append("skills")
    if len(info['degree']) == 0:
        sec_not_present.append("degree")
    if info['experience']==None:
        sec_not_present.append("experience")
    if len(info['projects']) == 0:
        sec_not_present.append('projects')
    context['sections_absent'] = sec_not_present
    if len(sec_not_present)>0:
        context['sections_absent_exist'] = True
    else:
        context['sections_absent_exist'] = False
    print(context['sections_absent_exist'])

    #count words
    if info['word_count']>=200:
        context['wordCount_ok'] = True
    else:
        context['wordCount_ok'] = False
    context['wordCount'] = [info['word_count']]
    #education
    context['degreeCount'] = [len(info['degree'])]
    if len(info['degree'])==0:
        context['isEducated'] = False
    else:
        context['isEducated'] = True
    #skills
    context['skills_count'] = [len(info['skills'])]
    if(context['skills_count'][0]>=5):
        context['skills_count_ok'] = True
    else:
        context['skills_count_ok'] = False

    # projects
    context['projects_count'] = [len(info['projects'])]
    if (context['projects_count'][0] >= 1):
        context['projects_count_ok'] = True
    else:
        context['projects_count_ok'] = False

    #experience
    if info['experience'] != None:
        context['experience_count'] = [len(info['experience'])]
    else:
        context['experience_count'] = [0]
    if (context['experience_count'][0] >=1):
        context['experience_count_ok'] = True
    else:
        context['experience_count_ok'] = False

    #score
    score = 0
    score = 6 - len(sec_not_present)
    if context['skills_count'][0]<=10:
        score = score + context['skills_count'][0]/10
    elif  context['skills_count'][0]>10:
        score = score + 1
    if context['experience_count'][0]<=5:
        score = score + context['experience_count'][0]/5
    elif  context['experience_count'][0]>5:
        score = score + 1
    if context['projects_count'][0]<=5:
        score = score + context['projects_count'][0]/5
    elif  context['projects_count'][0]>5:
        score = score + 1
    if context['degreeCount'][0]<=2:
        score = score + context['degreeCount'][0]/2
    elif  context['degreeCount'][0]>2:
        score = score + 1
    context['score'] = score*10
    print(score)



    return context