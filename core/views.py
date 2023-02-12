from django.shortcuts import render, redirect
from .parser2 import ParserModel,extract_skills,extract_experience
from .suggestions import find_suggestions
from .email_send import send_email
from .searchResumes import search_resumes
import random
import os
from django.core.files.storage import default_storage
from pymongo import MongoClient
from django.core.mail import EmailMessage, get_connection

#MoNGODB CONNECTION
try:
    client = MongoClient("mongodb+srv://vinubalan:vinubalan@resumes-cluster.7j616me.mongodb.net/?retryWrites=true&w=majority")
    db = client.test
    print("connected to mongo")
    resumes_db = db['resumes']
except:
    print("Connection Failed")
# Create your views here.
jobRolesList = []

context = {}
preview = {
    "path": ""
}
send_mail_ids = []
# computer_vision_skills = {"job":"computer_vision_engineer","skills":['opencv','computer vision','tensorflow','yolo','dlib','python']}
# full_stack_skills = {"job":"full_stack_developer","skills":['reactjs','angular','mongodb','sql','vuejs','firebase']}
# machine_learning_skills = {"job":"machine_learning_engineer","skills":['scikit learn','deeplearning','tensorflow','pytorch','machine learning']}
# tot_skill_job_skills = []
# tot_skill_job_skills.append(computer_vision_skills)
# tot_skill_job_skills.append(full_stack_skills)
# tot_skill_job_skills.append(machine_learning_skills)
#similarity Graph Structure
similarity = {
    "full_stack_developer":["full_stack_developer","java_developer","software_engineer","software_developer","mobile_app_developer","test_analyst"],
    "java_developer":["java_developer","full_stack_developer","software_engineer","software_developer","mobile_app_developer","test_analyst"],
    "machine_learning_engineer":["machine_learning_engineer","data_scientist","data_analyst","data_engineer","computer_vision_engineer"],
    "research_intern": ["research_intern","software_engineer","software_developer","mobile_app_developer","data_scientist","data_analyst","data_engineer","computer_vision_engineer"],
    "computer_vision_engineer":["computer_vision_engineer","data_scientist","data_analyst","data_engineer","machine_learning_engineer"],
    "data_scientist":["software_engineer","software_developer","mobile_app_developer","data_scientist","data_analyst","data_engineer","computer_vision_engineer"],
    "mobile_app_developer":["research_intern","software_engineer","software_developer","mobile_app_developer","full_stack_developer","test_analyst"],
    "test_analyst":["test_analyst","java_developer","full_stack_developer","software_engineer","software_developer","mobile_app_developer"],
    "software_developer":["software_developer","test_analyst","java_developer","full_stack_developer","software_engineer","mobile_app_developer"]
}
bachelors = ["btech-",'btech','b.tech','b. tech','b tech','b. tech','bachelor of engineering','be','b.e','b . e','b.e',
             'b e','bachelor technology','bachelor degree','bachelors degree',"bachelor science",'bachelors',"bs",'b.s',
             'b s','B.ED','bed','intermediate','b ed','B ED', "bsc",'B.SC','b. sc','b.sc',"b.s.c","ba","b.a",
             "bachelor of arts",'Bachelor of Arts',"bcom","b.com",'b ca','b.cs','bca','bachelor',"BCA","bca",'b.pharmacy','b pharmacy','b.pharm',
             'mtech', 'm tech', 'm.tech', 'm tech', 'm.tech', 'msc', "ms", "m.s", "M.Sc", "m.s.", 'm.sc', 'msc',
             'm. sc', "masters in", "master of science", 'post graduate',
             "mcom", "m.com", "m com", "mba", "m.b.a", "Masters", "masters", "master", "mca", "MCA", 'mphil', 'm phil'
             ]
masters = ['mtech','m tech','m.tech','m tech','m.tech','msc',"ms","m.s","M.Sc","m.s.",'m.sc','msc','m. sc',"masters in","master of science",'post graduate',
           "mcom","m.com","m com","mba","m.b.a","Masters","masters","master","mca","MCA",'mphil','m phil',"phd","ph.d.","Doctorate",'post graduate','doctorate']
phd = ["phd","ph.d.","Doctorate",'post graduate','doctorate']
def index(request):
    findings = {
        "results": [],
        "posted": False,
        "send": False,
        "query": []
    }

    if request.method=='POST':
        try:
            query = request.POST['searchQuery']
            designation = request.POST['designationQuery']
        except:
            jobdes = request.POST['jobdescription']
            query = extract_skills(jobdes)
            print(query)
            designation = request.POST['designationQuery']
        print(designation)
        location = request.POST['searchLocation']
        location = location.lower()
        designation_init = designation
        exp_type = request.POST['experience']
        education = request.POST['education']
        try:
            query = query.lower().split(',')
        except:
            pass
        findings['query'] = query
        designation = designation.replace(" ", "_")
        designation = designation.lower()
        mails = []
        for des in similarity[designation]:
            collection = db[des]
            vals = collection.find({})
            for val in vals:
                print(val['name'])
            print("-----------------------------")
            res_skills = collection.find(
                {"$and":[{"skills": {"$elemMatch": {"$in": query}}}, {"location": {"$eq": location}}]})
            # res_skills = collection.find({"skills": {"$elemMatch": {"$in": query}}})
            for x in res_skills:
                good_match = 0
                for skill in x['skills']:
                    if skill in query:
                        good_match += 1
                x['goodFit'] = good_match
                if x['mailid'] not in mails:
                    findings["results"].append(x)
                    mails.append(x["mailid"])
            res_exp = findings["results"]
            # print("after getting skills scored")
            # print(findings['results'])
            # for x in res_exp:
            #     print(x['name'])
            for x in res_exp:
                try:
                    if des in x['experience']['designation'].lower().replace(" ","_"):
                        x['goodFit'] += 3
                except:
                    pass
            tmp = []
            for x in findings['results']:
                if x['experience']:
                    print(len(x['experience']))
                    if len(x['experience'])>=1:
                        if exp_type=="experienced":
                            tmp.append(x)
                    else:
                        if exp_type=="fresher":
                            tmp.append(x)
                else:
                    if exp_type == "fresher":
                        tmp.append(x)
            findings['result'] = tmp
            #
            # tmp=[]
            # # print(findings['results'])
            # # print("M.Sc" in bachelors)
            # for x in findings['results']:
            #     try:
            #         # print(x['degree']['education'])
            #         if education=="bachelors":
            #             for i in bachelors:
            #                 if x['degree']['education']==i:
            #                     tmp.append(x)
            #         elif education=='masters':
            #             for i in masters:
            #                 if x['degree']['education'] == i:
            #                     tmp.append(x)
            #         elif education == 'phd':
            #             for i in phd:
            #                 if x['degree']['education'] == i:
            #                     tmp.append(x)
            #     except:
            #         print(x['degree'][0]['education'])
            #         if education=="bachelors":
            #             for i in bachelors:
            #                 if x['degree'][0]['education'] == i:
            #                     tmp.append(x)
            #         elif education=='masters':
            #             for i in masters:
            #                 if x['degree'][0]['education'] == i:
            #                     tmp.append(x)
            #         elif education == 'phd':
            #             for i in masters:
            #                 if x['degree'][0]['education'] == i:
            #                     tmp.append(x)
            # findings['results'] = tmp
            # print("after db find")
            # print(findings['results'])

            # res_exp = collection.find({"experience.designation": {"$in": [designation_init]}})
            # print(findings['results'])
            # for x in res_exp:
            #     print(x)
            #     if x not in findings['results']:
            #         print("From",designation,x['name'])
            #         findings["results"].append(x)
            # for x in res_exp:
            #     good_match = 0
            #     for exp in x['experience']['designation']:
            #         if exp in query:
            #             good_match += 3
            #     x['goodFit'] += good_match
            # res_company = collection.find({"experience.company": {"$in": query}})
            # for x in res_company:
            #     if x not in findings['results']:
            #         findings["results"].append(x)
        findings['send'] = True
        send_mail_ids = mails
        best_fit = 1
        for x in findings['results']:
                # print(x['goodFit'])
            if x['goodFit'] >= best_fit:
                best_fit = x['goodFit']
            # print(best_fit)
        if len(query) == 1:
            for x in findings['results']:
                x['bestFit'] = True
        else:
            for x in findings['results']:
                if x['goodFit'] <= best_fit * 0.5:
                    x['bestFit'] = False
                else:
                    x['bestFit'] = True
        findings['results'] = sorted(findings['results'], key=lambda i: i['goodFit'], reverse=True)
            # findings['results'] = list(set(findings['results']))
        if len(findings['results']) == 0:
                findings = {
                    "posted": True
                }
        # else:
        #     findings = {
        #         "posted": True
        #     }
        # for q in query:
        #     q = q.replace(" ","_")
        #     if q in
        print(query)

        return render(request, 'index.html', context=findings)
    return render(request, 'index.html',context = findings)

def resume_upload(request):
    global context
    context = {
        "isSubmitted": True
    }
    if request.method == 'POST' and request.FILES['resume']:
        username = request.POST['username']
        mailid = request.POST['mailid']
        jobRole = request.POST['designation']
        jobRole = jobRole.replace(" ","_")
        jobRole = jobRole.lower()
        if jobRole in db.list_collection_names():
            collection = db[jobRole]
            print("The database already exists.")
        else:
            # Create Collection
            db['designations'].insert_one({
                "job": jobRole
            })
            collection = db[jobRole]
            jobRolesList.append(jobRole)
        found_resumes = collection.find_one({"mailid": mailid})
        print(found_resumes)
        if found_resumes:
            delete_filename = found_resumes['resume']
            try:
                os.remove('resumes/'+delete_filename)
            except:
                pass
            collection.delete_one({
                "mailid": mailid
            })
        f = request.FILES['resume']
        filename = str(f)

        code = random.randint(1000, 9999)
        with default_storage.open('resumes/'+ str(code) + filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        final_parsed = ParserModel.parse_resume('resumes/' + str(code) + filename)
        if final_parsed['contact_number']:
            contact = final_parsed['contact_number']
        else:
            contact = ''
        # print(final_parsed)
        info = {
            "name": username,
            "mailid": mailid,
            "resume": str(code)+filename,
            "contactNumber": contact,
            "linkedIn": final_parsed['linkedIn-link'],
            "gender": final_parsed['gender'],
            "nationality": final_parsed['nationality'],
            "marital_status": final_parsed['marital status'],
            "skills": final_parsed['skills'],
            "degree": final_parsed['degree'],
            "experience": final_parsed['experience'],
            "projects": final_parsed['projects'],
            "githubLinks": final_parsed['github_links'],
            "location": final_parsed['location'],
            "word_count": final_parsed['word_count'],
            "bestFit": final_parsed['bestFit'],
            "goodFit": 0
        }
        collection.insert_one({
            "name": username,
            "mailid": mailid,
            "resume": str(code)+filename,
            "contactNumber": contact,
            "linkedIn": final_parsed['linkedIn-link'],
            "gender": final_parsed['gender'],
            "nationality": final_parsed['nationality'],
            "marital_status": final_parsed['marital status'],
            "skills": final_parsed['skills'],
            "degree": final_parsed['degree'],
            "experience": final_parsed['experience'],
            "projects": final_parsed['projects'],
            "githubLinks": final_parsed['github_links'],
            "location": final_parsed['location'],
            "word_count": final_parsed['word_count'],
            "bestFit": final_parsed['bestFit'],
            "goodFit": 0
        })
        print("resume uploaded")
        context_ = find_suggestions(info)
        context = context_
        return redirect('/suggestions')

    return render(request, 'upload.html',context=context)

def suggestions(request):
    print(context)
    return render(request, 'suggestions.html',context=context)

def composemail(request):
    if request.method=='POST':
        company_name = request.POST['companyname']
        message_text = request.POST['message']
        send_email(["vinubalan.aids@citchennai.net"],company_name,message_text)
        redirect('/')
    return render(request, 'composeMail.html')