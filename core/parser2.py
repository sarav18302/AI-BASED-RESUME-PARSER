from .pdf_to_text import convert_to_text
from .docx_to_text import docx_to_text
from resume_parser import resumeparse
import locationtagger
import os
import re
import os
import nltk
import spacy
from spacy.matcher import Matcher
import json
import datetime
import spacy
from spacy import displacy

PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{7,}[0-9]')

# actual_file_name = "AtulSharma_4640222_-02_02-_1.pdf"
# file_name = "100-Original-Resumes/"+actual_file_name


#print(resume_text)


# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

word_count = 0

def extract_name(resume_text):
    global word_count
    resume_text.strip()
    word_count = len(resume_text.split())
    resume_text = resume_text.lower().replace(':','')
    resume_text = resume_text.lower().replace('.', ' ')
    resume_text = resume_text.lower().replace('‰', '')
    resume_text = resume_text.lower().replace('-','')
    resume_text = resume_text.lower().replace('_', '')
    resume_text = resume_text.lower().replace('  ', '')
    resume_text = resume_text.lower().replace('\n', ' ')
    resume_text = resume_text.lower().replace('msc', ' ')
    resume_text = resume_text.lower().replace('curriculum vitae', '')
    resume_text = resume_text.lower().replace('curriculam vitae', '')
    resume_text = resume_text.lower().replace('contact', '')
    resume_text = resume_text.lower().replace('emailid', '')
    resume_text = resume_text.lower().replace('summary', '')
    resume_text = resume_text.lower().replace('india', '')
    resume_text = resume_text.lower().replace('mobile', '')
    resume_text = resume_text.lower().replace('linkedin', '')
    resume_text = resume_text.lower().replace('andhra pradesh', '')
    resume_text = resume_text.lower().replace('chennai', '')
    resume_text = resume_text.lower().replace('email', '')
    resume_text = resume_text.lower().replace('data', '')
    order = r'[0 - 9]'
    resume_text = re.sub(order, '', resume_text)
    resume_text = resume_text.lower().replace('curriculumvitae', '')
    resume_text = resume_text.lower().replace('professional experience', '')
    resume_text = resume_text.lower().replace('experience', '')
    resume_text = resume_text.lower().replace('skills', '')
    resume_text = resume_text.lower().replace('education', '')
    resume_text = resume_text.lower().replace('resume', '')
    resume_text = resume_text.lower().replace('working', '')
    resume_text = resume_text.lower().replace('coding manager resume', '')
    resume_text = resume_text.lower().replace('manager resume', '')
    resume_text = resume_text.lower().replace('java developer', '')
    resume_text = resume_text.lower().strip()

    nlp_text = nlp(resume_text[:36])
    temp_res = resume_text[:36].lower().split(' ')
    if 'name' in temp_res:
        for i in range(len(temp_res)):
            if temp_res[i]=='name':
                return temp_res[i+1]

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}]

    matcher.add('NAME', None, pattern)

    matches = matcher(nlp_text)
    names = []
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        names.append(span.text)
    taken_text = " ".join(names)
    final_text = ""
    if ".com" in taken_text or "@" in taken_text:
        for i in taken_text:
            if i.isalpha():
                final_text+=i
            else:
                return final_text
    return taken_text

def extract_phone_number(resume_text):
    resume_text  = resume_text.replace("-"," ")
    resume_text = resume_text.replace("/", " ")
    phone = re.findall(PHONE_REG, resume_text[:])
    phone = [num for num in phone if len(num)>8]
    phone = [num for num in phone if len("".join(num.split()))>8]
    if phone:
        number = ''.join(phone[0])

        if resume_text.find(number) >= 0 and len(number) < 20:
            return number
    return None

def extract_email(email):
    resume_text = email.replace("-", " ")
    resume_text = resume_text.replace(":", " ")
    resume_text = resume_text.replace("email", " ")
    resume_text = resume_text.replace("id", " ")
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", resume_text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

def extract_linkdin_links(resume_text):
    word_tokens = nltk.tokenize.word_tokenize(resume_text)
    linkedIn_links = [l for l in word_tokens if "linkedin.com/" in l.lower()]
    if len(linkedIn_links)!=0:
        return linkedIn_links
    else:
        return ["null",1]

#skills
SKILLS_DB = [
    'microdoft office','microsoft word','program development','technical writing',
    'machine learning','dbms','dbms/sql','sql','data structure',
    'data science','datascience','scikit','matlab','microsoft office suite','microsoft visual basic',
    'python','numpy','pandas','powerbi','power bi','adobe fireworks',
    'computer vision','deep learning','kotlin','mysql','mongodb',
    'nlp','public speaking','critical thinking','creativity',
    'natural language processing','data visualization','feature engineering',
    'data analytics','negotiation','feature selection',
    'data preprocessing','database','cloud computing',
    'opencv','adaptability','collaboration','blex','automation','statistics',
    'c','python','diagnostic analysis', 'linux','unix',
    'c++','c/c++','ar caller','spring mvc','spring boot','spring framework',
    'java','swift','ms-powerpoint','ms-excel',
    'javascript','wordpress','sass','cloud technologies','azure cloud',
    'php','node.js','jsf','j2ee',
    'perl','ajax','team working','business intelligence',
    'scala','sap','devops','tableau',
    'leadership','problem solving','communication',
    'web design','ui/ux design','web development','front end web development',
    'full stack web development','reactjs','angular','nodejs','react js','node js','java script',
    'android app development','app development','android studio','flutter',
    'html','css','jquery','bootstrap','material ui',
    'deep learning','vb.net','.net','asp.net',
    'cnn','convolutional neural networks','tensor flow','tensorflow','yolo',
    'rnn','recurrent neural networks','artificial neural networks',
    'lstm','team leadership','icd 10', 'cpt','hcps codes',
    'ar','augumented reality','unity 3d', 'web design','mysql','database',
    'vr','virtual reality','Spring Boot', 'Hibernate', 'Maven', 'Spring Mvc','Spring', 'SVN', 'Restful Webservices',
    'block chain','big data','spark','hadoop','ibm watson','ibm cloud','aws',
    'word',"game programing","game development",
    'excel','linux','oracle','s-frame','epanet','culvert master','stormcad','cad','flowmaster','autocad',
    'english','tamil','hindi','german','japanese','french',
    'visual studio','eclipse','vhdl','assembly', 'security','networking','operating system','rdbms','dns','ipsec','bgp',
    'vpn','load balancing','distributed system','distributed system'
]
Job_skills_db  = [
    'microdoft office','microsoft word','program development','technical writing',
    'machine learning','dbms','dbms/sql','sql','data structure',
    'data science','datascience','scikit','matlab','microsoft office suite','microsoft visual basic',
    'python','numpy','pandas','powerbi','power bi','adobe fireworks',
    'computer vision','deep learning','kotlin','mysql','mongodb',
    'nlp','public speaking','critical thinking','creativity',
    'natural language processing','data visualization','feature engineering',
    'data analytics','negotiation','feature selection',
    'data preprocessing','database',
    'opencv','adaptability','collaboration',
    'c','python','diagnostic analysis',
    'c++','c/c++','ar caller','spring mvc','spring boot','spring framework',
    'java','swift','ms-powerpoint','ms-excel',
    'javascript','wordpress','sass','cloud technologies','azure cloud',
    'php','node.js','jsf','j2ee',
    'perl','ajax','team working','business intelligence',
    'scala','sap','devops','tableau',
    'leadership','problem solving',
    'web design','ui/ux design','web development','front end web development',
    'full stack web development','reactjs','angular','nodejs','react js','node js','java script',
    'android app development','app development','android studio','flutter',
    'html','css','jquery','bootstrap','material ui',
    'deep learning','vb.net','.net','asp.net',
    'cnn','convolutional neural networks','tensor flow','tensorflow','yolo',
    'rnn','recurrent neural networks','artificial neural networks',
    'lstm','team leadership','icd 10', 'cpt','hcps codes',
    'ar','augumented reality','unity 3d',
    'vr','virtual reality','Spring Boot', 'hibernate', 'maven', 'spring mvc','spring', 'svn', 'restful webservices',
    'block chain','big data','spark','hadoop','ibm watson','ibm cloud','aws',
    'word',"game programing","game development",
    'excel','linux','oracle','s-frame','epanet','culvert master','stormcad','cad','flowmaster','autocad',
    'visual studio','eclipse','vhdl','assembly'
]
def extract_skills(resume_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(resume_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    # we create a set to keep the results in.
    found_skills = set()

    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in SKILLS_DB:
            found_skills.add(token.lower())

    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in SKILLS_DB:
            found_skills.add(ngram.lower())

    return list(found_skills)
def experience_skills(resume_text,experience):
    # if len(experience)==0:
    #     return []
    stop_words = set(nltk.corpus.stopwords.words('english'))
    index_list = []
    try:
        for ex in experience:
            index_list.append(resume_text.lower().find(ex))
        final_index = min(index_list)
        resume_text = resume_text[final_index:final_index+1000]
    except:
        resume_text = resume_text[100:]
    word_tokens = nltk.tokenize.word_tokenize(resume_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    # we create a set to keep the results in.
    found_skills = set()

    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in Job_skills_db:
            found_skills.add(token.lower())

    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in Job_skills_db:
            found_skills.add(ngram.lower())
    if len(found_skills)==0:
        resume_text = resume_text[150:]
        word_tokens = nltk.tokenize.word_tokenize(resume_text)

        # remove the stop words
        filtered_tokens = [w for w in word_tokens if w not in stop_words]

        # remove the punctuation
        filtered_tokens = [w for w in word_tokens if w.isalpha()]

        # generate bigrams and trigrams (such as artificial intelligence)
        bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

        # we create a set to keep the results in.
        found_skills = set()

        # we search for each token in our skills database
        for token in filtered_tokens:
            if token.lower() in Job_skills_db:
                found_skills.add(token.lower())

        # we search for each bigram and trigram in our skills database
        for ngram in bigrams_trigrams:
            if ngram.lower() in Job_skills_db:
                found_skills.add(ngram.lower())
    found_skills = list(found_skills)
    # if 'tamil' in found_skills:
    #     found_skills.remove('tamil')
    # elif 'english' in found_skills:
    #     found_skills.remove('english')
    # elif 'hindi' in found_skills:
    #     found_skills.remove('hindi')
    return list(found_skills)

#experience
EXPERIENCE_DB = [
    'machine learning engineer','ml engineer','machine learning intern','service manager','service manager',"junior executive",
    'research intern','sales professional','research associate','engineering executive','software engineering intern','web developer intern',
    'junior data scientist','data scientist','data science intern','maintenance technician','software engineer','systems engineer',
    'junior ai research scientist','ai research scientist','lab technician','lab assistant',"professor","mentor","teacher",'programmer',
    'data analyst','data engineer','.net developer','business analyst','data analyst intern','data engineer intern','business analyst intern',
    'resume writer','ambassador','sales assistant','sales manager','supervisor','assurance inspector','software developer','software engineer',
    'sds','developer analyst','java developer','team lead','training officer','assistant manager','pharmacist','systems engineer',
    'system engineer','ar caller','java programming intern','professor','trainee decision scientist','java developer',
    'team coach','team leader','software developer','quality analyst','process associate','professor','data analyst','software asssociate','systems engineer',
    'quality analyst','cloud engineer','client specialist','assistant manager','it recruiter','administrative assistant','devops engineer','developer analyst',
    'pharmacist','mentor','assistant manager','junior executive','business analyst',
    'ar caller','ambassador','ar executive'

]
def extract_experience(resume_text):
    resume_text = resume_text.replace("-", " ")
    resume_text = resume_text.replace("/", " ")
    resume_text = resume_text.replace(",", " ")
    resume_text = resume_text.replace("  ", " ")
    resume_text = resume_text.replace("%", " ")
    resume_text = resume_text.replace(" at ", " ")
    resume_text = resume_text.replace(" a ", " ")
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(resume_text[150:])
    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]
    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 1, 3)))

    # we create a set to keep the results in.
    found_EXPERIENCE = []

    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in EXPERIENCE_DB:
            found_EXPERIENCE.append(token.lower())

    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        #print(ngram)
        if ngram.lower() in EXPERIENCE_DB or ngram.lower()=='software developer' or ngram.lower()=='software engineer':
            found_EXPERIENCE.append(ngram.lower())
    #print(word_tokens)
    print(found_EXPERIENCE)
    return found_EXPERIENCE
locations = ['andhra pradesh','hyderabad','arunachal pradesh','assam','dispur','bihar','patna','chhattisgarh','goa','gujarat','gandhinagar','haryana','chandigarh','himachal pradesh','jammu and kashmir','jharkhand','karnataka','bengaluru','kerala',
             'tamil nadu','bangalore','coimbatore','chennai','bengaluru','karnataka','pune','deccan','vellore','jaipur']
def get_company(resume_text,experience):
    max_le = 0
    nlp = spacy.load('en_core_web_sm')
    res_text = ''
    res_text += resume_text
    sentences = resume_text.split("\n")
    sentences = [w for w in sentences if w != '']
    experience_list = []
    timeline = []
    company_name = ""
    location = set()
    location_name = ""
    found_COMPANY = []
    company = []
    for ex in experience:
        for line in range(len(sentences)):
            if ex.lower() in sentences[line].lower():
                print(sentences[line])
                company.append(sentences[line-3]+" "+sentences[line-2]+" "+sentences[line-1]+" "+sentences[line]+" "+ sentences[line + 1]+" "+sentences[line+2])
        try:
            sentence = company[-1]
        except:
            sentence = sentences[line]
        if len(sentence.title())!=0:
            doc = nlp(sentence.title())
            for ent in doc.ents:
                if ent.label_ == 'GPE':
                    location.add(str(ent))
                    location_name = str(ent)
        stop_words = set(nltk.corpus.stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(sentence)

        education_label = False
        # we search for each token in our skills database
        bigrams_trigrams = list(map(' '.join, nltk.everygrams(word_tokens, 2, 3)))

        # we create a set to keep the results in.

        # we search for each token in our skills database
        for i in range(len(word_tokens)):
            # if word_tokens[i].lower()=='hospital':
            #     if word_tokens[i-1].lower()=='medical':
            #         company_name = word_tokens[i - 2].title() + " " +word_tokens[i - 1].title() + " " + word_tokens[i].lower()
            #     else:
            #         company_name = word_tokens[i - 1].title() + " " + word_tokens[i].lower()
            #     found_COMPANY.append(company_name)
            #     break
            if word_tokens[i].lower() in ["autotech","infotech","technology","technologies",'group',"groups","company","startup","international","pvt",'private',"school","college","corporation",'health','healthcare',"tech","multinational","industry","solutions","industries",'co.','co']:

                if word_tokens[i-1].isalpha():
                    if word_tokens[i-1].lower()=='our' or word_tokens[i-1].lower()=='in' or  word_tokens[i-1].lower()=='my' or word_tokens[i-1].lower()=='present' or word_tokens[i-1].lower()=='.' or word_tokens[i-1].lower()=='and':
                        pass
                    elif word_tokens[i - 1].lower() == 'services':
                        if word_tokens[i-2].lower()=='management':
                            company_name = word_tokens[i - 3].title() + " " +word_tokens[i - 2].title() + " " + word_tokens[i - 1].title() + " " + word_tokens[i].title()
                            break
                    elif word_tokens[i-1].lower()=='management':
                        company_name = word_tokens[i - 2].title() + " " +word_tokens[i - 1].title() + " " + word_tokens[i].title()
                    elif word_tokens[i - 1].lower() == 'production':
                        company_name = word_tokens[i - 2].title() + " " + word_tokens[i - 1].title() + " " + word_tokens[i].title()
                        break
                    else:
                        company_name = word_tokens[i-1].title()+" "+word_tokens[i].title()
                else:
                    company_name =  word_tokens[i - 1].title() + " " + word_tokens[i].title() + " " + word_tokens[i+1].title()
                found_COMPANY.append(company_name)

            if word_tokens[i].lower()=='soft':
                company_name = word_tokens[i - 1].title() + " " + word_tokens[i].lower()
                found_COMPANY.append(company_name)
            if word_tokens[i].lower()=='services':
                if word_tokens[i-1].lower()=='management':
                    company_name = word_tokens[i - 3].title() + " " +word_tokens[i - 2].title() + " " +word_tokens[i - 1].title() + " " + word_tokens[i].lower()
                elif word_tokens[i-1].lower()=='global':
                    company_name = word_tokens[i - 2].title() + " " +word_tokens[i - 1].title() + " " + word_tokens[i].lower()
                elif word_tokens[i-1].lower()=='consultancy':
                    company_name = word_tokens[i - 2].title() + " " +word_tokens[i - 1].title() + " " + word_tokens[i].lower()
                else:
                    company_name = word_tokens[i - 1].title() + " " + word_tokens[i].lower()
                found_COMPANY.append(company_name)
            if word_tokens[i].lower()=='limited':
                if word_tokens[i-1].lower()=='private':
                    company_name = word_tokens[i - 4].title() + " " +word_tokens[i - 3].title() + " " +word_tokens[i - 2].title() + " " +word_tokens[i - 1].title() + " " + word_tokens[i].lower()
                    break
            if i<len(word_tokens):
                if word_tokens[i].lower() == 'university' and word_tokens[i+1].lower() == 'of':
                    company_name = "University of " +word_tokens[i + 2].title()
                    found_COMPANY.append(company_name)
                    break
            if word_tokens[i].lower() in ['university']:
                company_name = word_tokens[i - 2].title() + " " +word_tokens[i - 1].title() + " " + word_tokens[i].title()
                found_COMPANY.append(company_name)
                break
            if ".ai" in word_tokens[i].lower() or ".com" in word_tokens[i].lower() and "linkedin" not in word_tokens[i].lower() or ".io" in word_tokens[i].lower() or ".inc" in word_tokens[i].lower():
                if "github.com" in word_tokens[i].lower() or "google.com" in word_tokens[i].lower() or "linkdin" in word_tokens[i].lower():
                    pass
                else:
                    company_name = word_tokens[i-1]+word_tokens[i]
                    found_COMPANY.append(company_name)
                    break
            if "microsoft" in word_tokens[i].lower():
                company_name = word_tokens[i]
                found_COMPANY.append(company_name)
                break
            if "google" in word_tokens[i].lower():
                company_name = word_tokens[i]
                found_COMPANY.append(company_name)
                break
            if "cognizant" in word_tokens[i].lower():
                company_name = word_tokens[i]
                found_COMPANY.append(company_name)
                break
            if "ibm" in word_tokens[i].lower():
                company_name = word_tokens[i]
                found_COMPANY.append(company_name)
                break
            if "infosys" in word_tokens[i].lower():
                company_name = word_tokens[i]
                found_COMPANY.append(company_name)
                break
            if "tcs" in word_tokens[i].lower():
                company_name = word_tokens[i]
                found_COMPANY.append(company_name)
                break
            if word_tokens[i].lower()=='health':
                company_name = word_tokens[i - 1].title() + " " + word_tokens[i].lower()
                found_COMPANY.append(company_name)
        month =[]
    # for ex in experience:
    #     for line in range(len(sentences)):
    #         if ex.lower() in sentences[line].lower():
    #             company.append(
    #                 sentences[line - 3] + " " + sentences[line - 2] + " " + sentences[line - 1] + " " + sentences[
    #                         line] + " " + sentences[line + 1] + " " + sentences[line + 2])
        try:
            sentence = company[-1]
        except:
            sentence = sentences[line]
        try:
            sentence = sentence.lower()
            res_text = res_text.replace("-", " ")
            res_text = res_text.replace("'", " ")
            till_date  = False
            if 'present' in sentence or 'till date' in sentence or 'till now' in sentence:
                till_date = True
            res_text = res_text.split()
            for i in res_text:
                if 'jan' in i.lower():
                    month.append('January')
                elif 'feb' in i.lower():
                    month.append('February')
                elif 'march' in i.lower():
                    month.append('March')
                elif 'apr' in i.lower():
                    month.append('April')
                elif 'may' in i.lower():
                    month.append('May')
                elif 'jun' in i.lower():
                    month.append('June')
                elif 'july' in i.lower():
                    month.append('July')
                elif 'aug' in i.lower():
                    month.append('August')
                elif 'sept' in i.lower():
                    month.append('September')
                elif 'oct' in i.lower():
                    month.append('October')
                elif 'nov' in i.lower():
                    month.append('November')
                elif 'decem' in i.lower():
                    month.append('December')
            print(month)
            print(till_date)
        except:
            pass
        till_date = False
        nums = re.findall(r'[1-2][0-9][0-9][0-9]', sentence)
        nums = [int(n) for n in nums]
        nums = [w for w in nums if int(w) < 2030 and int(w) > 1990 ]
        nums = list(set(nums))
        nums.sort()
    # try:
    #     nums = [str(min(nums)),str(max(nums))]
    # except:
    #     nums = []
        if len(month)>0:
            try:
                if till_date or min(nums)==max(nums):
                    nums = [month[0] + " "+str(min(nums))+" - Till date"]
                else:
                    nums[0] = month[0] + " "+str(min(nums))
                    nums[1] = month[1] + " " + str(max(nums))
                    print(nums)
            except:
                pass
        else:
            try:
                nums = [str(min(nums)), str(max(nums))]
            except:
                nums = []
        experience_list.append({"designation":ex,"company":company_name,"location":location_name,"duration":nums})
    # return list(found_COMPANY),list(location),timeline[:len(found_COMPANY)]
    #return experience_list[0]
    # if len(experience_list)>1:
    #     print("tried")
    #     indexer = 0
    #     for le in range(len(experience_list)):
    #         try:
    #             print(experience_list[le]["duration"][-1])
    #             if int(experience_list[le]["duration"][-1])>max_le:
    #                 max_le = int(experience_list[le]["duration"][-1])
    #                 indexer = le
    #         except:
    #             pass

        # return experience_list[0]
        if len(experience_list)==1:
            return experience_list[0]
        else:
            if len(experience)>0:
                experience_list.append({"designation": experience[0], "company": "", "location": "", "duration": []})
                return experience_list[0]
            else:
                return []
#Gender
def extract_gender(resume_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(resume_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
    gender_label = False
    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower()=='gender' or token.lower()=='sex':
            gender_label = True
        if gender_label:
            if token.lower()=='male' or token.lower()=='m':
                return 'male'
            elif token.lower()=='female' or token.lower()=='f':
                return 'female'
def extract_status(resume_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(resume_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
    gender_label = False
    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower()=='marital' or token.lower()=='status':
            gender_label = True
        if gender_label:
            if token.lower()=='single' or token.lower()=='unmarried':
                return 'single'
            elif token.lower()=='married':
                return 'married'
    for token in filtered_tokens:
        if token.lower() == 'single' or token.lower() == 'unmarried':
            return 'single'
        elif token.lower() == 'married':
            return 'married'

#Nationality
def extract_Nationality(resume_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(resume_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # we create a set to keep the results in.
    Nationality_label = False
    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower()=='indian':
            return 'indian'
        elif token.lower()=='anglo indian':
            return 'anglo indian'
        elif token.lower() == 'american':
            return 'american'
    for token in filtered_tokens:
        if token.lower()=='indian' or token.lower()=='india':
            return 'indian'
        elif token.lower()=='anglo indian':
            return 'anglo indian'
        elif token.lower() == 'american':
            return 'american'

#Education
#experience
EDUCATION_DB = [
    "btech-",'btech','b.tech','b. tech','b tech','b. tech','bachelor of engineering','mtech','m tech','m.tech','be','b.e','b . e','b.e','b e','bachelor technology','bachelor degree','bachelors degree','m tech','m.tech',
    "bachelor science",'bachelors',"bs",'b.s','b s','B.ED','bed','intermediate','b ed','B ED','msc',"ms","m.s","m.s.",'m.sc','msc','m. sc',"masters in","master of science","phd","ph.d.","Doctorate",'post graduate',
    "bsc",'B.SC','b. sc','b.sc',"b.s.c","ba","b.a","bachelor of arts",'Bachelor of Arts',"bcom","b.com","mcom","m.com","m com","mba","m.b.a","Masters","masters","master",'ph.d','ca','c a','b ca','b.cs','bca',
    'pgd',"diploma","higher secondary","12th","10th","hsc","h.s.c","sslc","b.sc",'hss','bachelor',"mca","MCA","BCA","bca",'b.pharmacy','b pharmacy','b.pharm','mphil','m phil'

]
STREAM_DB = [
'CSE','Computer Science','COMPUTER SCIENCE','Computer Application','COMPUTER APPLICATION','Artificial Intelligence','Artiﬁcial Intelligence',
    'IT','Information Technology','INFORMATION TECHNOLOGY','Accountant','Accountancy','Electronics Communications','Electronics Telecommunications',
    'AI DS','AI and DS','ARTIFICIAL INTELLIGENCE',"Artificial Intelligence","Artificial Intelligence & DataScience","Artificial Intelligence Datascience","artificial intelligence",
    'MECH',"Mechanical Engineering","Mechanical","MECHANICAL ENGINEERING",'ELECTRICAL ENGINEERING','Costume Design',
    "EEE","ELECTRICAL ELECTRONICS",'electronics communication','Electrical Engineering','Electricals & Electronics',"Electrical Electronics",'Electrical Electronics',"Electrical Electronical",
    "CIVIL","Civil","civil","Electrical and Communication","ECE","electrical communication",'Business Analytics',
    "biomedical","bme","BME","CSBS","Computer Science and Business Systems","Computer Science Business Systems",
    "stat","Business Administration",'Physics','Chemical Engineering','Aeronautics','AERONAUTICS','Electronics Communication',
    "physics","maths","mathematics","philosophy","business administration","MANAGEMENT",'pharmacy','Pharmacy','MANAGEMENT','Management',
    'accounting','history','HISTORY','SOCIALOGY','Socialogy','BUSINESS MANAGEMENT','Business Management','MARKETING',
    'BioMedical Engineering','Nursing','NURSING','Computer Applications','COMPUTER APPLICATIONS','Bio Medical',
    'Data Science','Pharmacy','pharmacy','PHARMACY','Biochemistry','Software Engineering','Life Sciences','Biotechnology'
]

def extract_education(resume_text):
    resume_text = resume_text.replace(","," ")
    resume_text = resume_text.replace("'", "")
    resume_text = resume_text.replace("-", " ")
    resume_text = resume_text.replace("/", " ")
    resume_text = resume_text.replace("(", " ")
    resume_text = resume_text.replace(")", " ")
    resume_text = resume_text.replace("&", " ")
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(resume_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words or w in "."]
    temp = filtered_tokens
    # remove the punctuation
    temp = [w for w in word_tokens if w.isalpha()]

    education_label = False
    # we search for each token in our skills database
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 4)))

    # we create a set to keep the results in.
    found_EDUCATION = set()
    found_STREAM = set()

    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in EDUCATION_DB:
            found_EDUCATION.add(token.lower())
        if 'BE' == token:
            found_EDUCATION.add(token.upper())
        if token in STREAM_DB:
            found_STREAM.add(token.upper())
        if "cbse" in token.lower():
            found_EDUCATION.add("hsc")
        if "hsc" in token.lower() or "12th" in token.lower():
            found_EDUCATION.add(token.lower())
        if "sslc" in token.lower() or "10th" in token.lower() or "ssc" in token.lower():
            found_EDUCATION.add(token.lower())

    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in EDUCATION_DB:
            found_EDUCATION.add(ngram.lower())
    for ngram in bigrams_trigrams:
        if ngram in STREAM_DB:
            found_STREAM.add(ngram.upper())
    if 'computer science and engineering' in resume_text.lower():
        found_EDUCATION.add('b.e')
    return list(found_EDUCATION),list(found_STREAM)

def extract_stream(resume_text,degree):
    sentences = resume_text.split("\n")
    sentences = [w for w in sentences if w != '']
    check = ''
    branch = ''
    discipline = ''
    graduation = ''
    cgpa = ''
    branch_set = []
    stream_set = []
    graduation_year = []
    found_STREAM = []
    for deg in degree:
        for i in range(len(sentences)):
            if deg in sentences[i].lower():
                check = sentences[i-1]+" "+sentences[i]+" "+sentences[i+1]
                check = check.replace(",", " ")
                check = check.replace("'", "")
                check = check.replace("-", " ")
                check = check.replace("/", " ")
                stop_words = set(nltk.corpus.stopwords.words('english'))
                word_tokens = nltk.tokenize.word_tokenize(check)
                filtered_tokens = [w for w in word_tokens if w not in stop_words or w in "."]
                for token in filtered_tokens:
                    if token in STREAM_DB:
                        #found_STREAM.append({'degree':deg.upper(),'dicipline':token.upper()})
                        branch = deg.upper()
                        discipline = token.upper()
                bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
                for ngram in bigrams_trigrams:
                    if ngram in STREAM_DB:
                        #found_STREAM.append({'degree':deg.upper(),'dicipline':ngram.upper()})
                        branch = deg.upper()
                        discipline = ngram.upper()
                nums = re.findall(r'[1-9]*[.]*[0-9]+', check)
                p_nums1 = re.findall(r'[1-9][0-9]*[.]*[0-9][%]+', check)
                p_nums2 = re.findall(r'[1-9][0-9]*[.]*[0-9]*[ ][%]+', check)
                p_nums=p_nums1+p_nums2
                for i in p_nums:
                    j = i.replace('%', '')
                    if float(j) > 99 or float(j) < 15:
                        try:
                            j = str(j) + "%"
                            p_nums.remove(j)
                        except:
                            pass
                            # j = str(j) + " %"
                            # p_nums.remove(j)
                nums = [w for w in nums if w != "" and float(w) < 10.0 and float(w) > 2.0 and w.count('.') == 1]
                if len(p_nums) > 0 or len(nums) > 0:
                    cgpa = p_nums + nums
                else:
                    cgpa = None
                nums = re.findall(r'[1-2][0-9][0-9][0-9]', check)
                if len(nums) > 0:
                    timeline = max(nums)
                else:
                    timeline = None
                if branch=='':
                    break
                if branch in branch_set and discipline in stream_set:
                    break
                else:
                    branch_set.append(branch)
                    stream_set.append(discipline)
                found_STREAM.append({'degree':branch,'discipline':discipline,'graduation year':timeline,'CGPA':cgpa})
                break
    return found_STREAM




Institutes = ['college',"arts and science","university","institute technology","institute of technology",'institute of technologies','iiit','iit','nit','vit','cit','mit',
              "school","school of engineering","arts and sciences","college of arts","college",'institute of arts','institute of science']

def get_institution(resume_text,universit_notfound):
    resume_text = resume_text.replace("(", "")
    resume_text = resume_text.replace(")", "")
    resume_text = resume_text.replace(",", " ")
    resume_text = resume_text.replace("'", "")
    resume_text = resume_text.replace(".", "")
    resume_text = resume_text.replace("-", " ")
    resume_text = resume_text.replace("'", "")
    resume_text = resume_text.replace("’", "")
    # print(resume_text)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(resume_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens]
    temp = filtered_tokens
    # remove the punctuation
    temp = [w for w in word_tokens if w.isalpha()]

    education_label = False
    # we search for each token in our skills database
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    # we create a set to keep the results in.
    found_institution = set()
    institute_txt = ''
    # we search for each token in our skills database
    for i in range(len(filtered_tokens)):
        if filtered_tokens[i].lower() in Institutes:
            #found_institution.add(filtered_tokens[i].lower())
            if "iit" == filtered_tokens[i].lower() or "nit" == filtered_tokens[i].lower() or "iiit" == filtered_tokens[i].lower():
                found_institution.add(filtered_tokens[i].upper())
            try:
                if "school" in filtered_tokens[i].lower():
                    if filtered_tokens[i - 2].isalpha():
                        found_institution.add(filtered_tokens[i - 4].title()+" "+filtered_tokens[i - 3].title()+" "+filtered_tokens[i - 2].title()+" "+filtered_tokens[i - 1].title()+" "+filtered_tokens[i].title())
                    else:
                        pass
                        #found_institution.add(filtered_tokens[i - 1] + " " + filtered_tokens[i])

            except:
                pass
            try:
                if filtered_tokens[i].lower() == "college":
                    if filtered_tokens[i+1].lower()=="of":
                        if filtered_tokens[i - 1].isalpha() and filtered_tokens[i-1].lower()!='science' and filtered_tokens[i-1].lower()!='present' and len(filtered_tokens[i-1])>2:
                            found_institution.add((filtered_tokens[i - 1] + " " + filtered_tokens[i] + " " + filtered_tokens[i + 1] + " " + filtered_tokens[i + 2]).title())
                        else:
                            found_institution.add((filtered_tokens[i] + " " + filtered_tokens[i + 1] + " " + filtered_tokens[i + 2] + " " + filtered_tokens[i + 3]).title())
                    else:
                        if filtered_tokens[i - 1].lower() == 'science' or filtered_tokens[i - 1].lower() == 'arts' or filtered_tokens[i - 1].lower()=='education' or filtered_tokens[i - 1].lower()=='after' or filtered_tokens[i - 1].lower()=='for' or filtered_tokens[i - 1].lower()=='my' or filtered_tokens[i - 1].lower()=='in':
                            pass
                        else:
                            found_institution.add((filtered_tokens[i - 1] + " " + filtered_tokens[i]).title())
            except:
                pass
        if "technology" in filtered_tokens[i].lower():
            if filtered_tokens[i-1].lower()=='of' and filtered_tokens[i-2].lower()=='institute':
                found_institution.add(filtered_tokens[i-3].title()+ " Institute of Technology")
        if "technologies" in filtered_tokens[i].lower():
            if filtered_tokens[i-1].lower()=='of' and filtered_tokens[i-2].lower()=='institute':
                found_institution.add(filtered_tokens[i-3].title()+ " Institute of Technologies")
        if "vidyalaya" in filtered_tokens[i].lower():
            found_institution.add(filtered_tokens[i-1].title() + " Vidhyalaya School")
        if "science" in filtered_tokens[i].lower() or "sciences" in filtered_tokens[i].lower():
            if filtered_tokens[i - 1].lower() == 'of' and filtered_tokens[i - 2].lower() == 'institute':
                if len(filtered_tokens[i - 3])<1:
                    found_institution.add(filtered_tokens[i - 4].title() + filtered_tokens[i - 3].title() + " Institute of Sciences")
                else:
                    found_institution.add(filtered_tokens[i - 3].title() + " Institute of Sciences")
        if "arts" in filtered_tokens[i].lower():
            if filtered_tokens[i - 1].lower() == 'of' and filtered_tokens[i - 2].lower() == 'institute':
                if len(filtered_tokens[i - 3]) < 1:
                    found_institution.add(
                        filtered_tokens[i - 4].title() + filtered_tokens[i - 3].title() + " Institute of Arts andSciences")
                else:
                    found_institution.add(filtered_tokens[i - 3].title() + " Institute of Arts andSciences")
        if universit_notfound:
            if "university" == filtered_tokens[i].lower():
                if filtered_tokens[i + 1].lower() == 'of':
                    found_institution.add(filtered_tokens[i].title() + " of "+filtered_tokens[i+2].title())
                elif filtered_tokens[i - 1].lower() == 'institute':
                    pass
                else:
                    found_institution.add(filtered_tokens[i-1].title() + " " + filtered_tokens[i].title())


    return list(found_institution)

def get_graduation(resume_text,education):
    sentences = resume_text.split("\n")
    sentences = [w for w in sentences if w != '']
    resume_text = "\n".join(sentences)
    resume_text = resume_text.replace("(", "")
    resume_text = resume_text.replace(")", "")
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(resume_text)
    # remove the stop words
    filtered_tokens = [w for w in word_tokens]
    nums = re.findall(r'[1-9]*[.]*[0-9]+',resume_text)
    p_nums = re.findall(r'[1-9][0-9]*[.]*[0-9][%]+', resume_text)
    for i in p_nums:
        j = i.replace('%','')
        if float(j)>99 or float(j)<25:
            j = str(j)+"%"
            p_nums.remove(j)
    nums = [w for w in nums if w!="" and float(w)<10.0 and float(w)>2.0 and w.count('.')==1]
    if len(p_nums)>0 or len(nums)>0:
        cgpa = list(set(p_nums+nums))
    else:
        cgpa = None
    timeline = []
    graduation_year = []
    sentences = resume_text.split("\n")
    sentences = [w for w in sentences if w!='']
    for edu in education:
        for line in range(len(sentences)):
            if edu.lower() in sentences[line].lower():
                graduation_year.append(sentences[line-1]+" "+sentences[line]+" "+ sentences[line + 1])
        try:
            sentence = graduation_year[-1]
            print(sentence)
        except:
            sentence = sentences[line]
        nums = re.findall(r'[1-2][0-9][0-9][0-9]', sentence)
        if len(nums)==0:
            sentence = resume_text
            nums = re.findall(r'[1-2][0-9][0-9][0-9]', sentence)
            nums = [w for w in nums if w != "" and int(w) < 2030 and int(w) > 2000]
            nums = list(set(nums))
        if len(nums)>0:
            nums = [w for w in nums if w != "" and int(w) < 2040 and int(w) > 2000]
            if len(nums)>0:
                timeline.append(max(nums))
    #cgpa = [float(x) for x in cgpa]
    return list(set(timeline)),cgpa
projects_words_DB = ['price','fraud','face','verification','covid','house','credit','card',"android","view",'ecommerce','test','solutions',"website","booking",'recognition',"ticket","created","made","developed","prediction","app","automation","program","analyzing","virtual assistant","web app","research paper","trained","website","model","detection","tracking","object","predictor","maker","guide","tracker","recommender","recommendation","system","bot","robot","automatic","self driving","visualising","visualizer","forecasting","help",'project','sender','reciever']
def extract_projects(resume_text):
    resume_text = resume_text.replace('\t'," ")
    sentences = resume_text[400:].split("\n")
    sentences = [w for w in sentences if w != '']
    projects_init = set()
    prev_line = 0
    for line in range(len(sentences)):
        count = 0
        for word in projects_words_DB:
            if word in sentences[line].lower():
                count+=1
        if count>2:
            if abs(line-prev_line)<3:
                pass
            else:
                prev_line = line
                projects_init.add(sentences[line])
        elif count>0 and ('prediction' in sentences[line].lower() or 'monitor' in sentences[line].lower() or 'system' in sentences[line].lower() and 'systems' not in sentences[line].lower()) and len(sentences[line])>10:
            if 'system' in sentences[line].lower() and ('operating' in sentences[line].lower() or 'computer' in sentences[line]):
                continue
            prev_line = line
            projects_init.add(sentences[line])
    word_tokens = nltk.tokenize.word_tokenize(resume_text)
    git_links = [l for l in word_tokens if "github.com/" in l.lower() or ".git" in l.lower()]
    return list(projects_init),git_links

def extract_location(resume_text):
    resume_text.strip()
    resume_text = resume_text.lower().replace(':', '')
    resume_text = resume_text.lower().replace('.', ' ')
    resume_text = resume_text.lower().replace('‰', '')
    resume_text = resume_text.lower().replace('-', '')
    resume_text = resume_text.lower().replace('_', '')
    resume_text = resume_text.lower().replace('  ', '')

    place_entity = locationtagger.find_locations(text=resume_text)
    states = place_entity.regions
    cities = place_entity.cities
    if len(cities)!=0:
        if cities[0].lower()=='java':
            location = "chennai"
        else:
            location = cities[0].lower()
    elif len(states)!=0:
        location = states[0].lower()
    else:
        location = "chennai"
    return location

def filter_education(education):
    ms, bs, dip = False, False, False
    for deg in education:
        deg = deg.replace("."," ")
        if deg in ['p.hd','phd','p hd','doctorate']:
            return 'P.hD'
    for deg in education:
        deg = deg.replace(".", " ")
        if deg in ['master','masters','ms','m s','msc','m sc','mba','mcom','m com','mca','m tech','mtech','m b a','m phil','ca','c a']:
            return 'M.Sc'
    for deg in education:
        deg = deg.replace(".", " ")
        if deg in ['m tech','mtech','m b a','m phil','ca','c a']:
            return 'M.Tech'
    for deg in education:
        deg = deg.replace(".", " ")
        if deg in ['m b a','m phil','ca','c a']:
            return 'M.B.A'
    for deg in education:
        deg = deg.replace(".", " ")
        if deg in ['m phil']:
            return 'M.phil'
    for deg in education:
        deg = deg.replace(".", " ")
        if deg == 'bca' or deg=='b ca':
            return 'BCA'
    for deg in education:
        deg = deg.replace(".", " ")
        if deg in ['ca','c a']:
            return 'CA'
    for deg in education:
        deg = deg.replace(".", " ")
        if deg in ['bs','bsc','bachelor','bachelors','b s','b sc','be','b e','btech','b tech','ba','b a','bca','b ca','b com','bcom']:
            return
    else:
        try:
            return education[0]
        except:
            return education


class ParserModel:
    def parse_resume(file_name):
        # print(file_name)
        try:
            resume_text = convert_to_text(file_name)
        except:
            try:
                resume_text = docx_to_text(file_name)
            except:
                print("unsupported file")
                return

        try:
            data = resumeparse.read_file(file_name)
        except:
            data = {"name":[],'university':[]}
        if len(data['name'])<=1 or 'name' in data['name'].lower().split() or 'objective' in data['name'].lower() or 'summary' in data['name'].lower() or 'vitae' in data['name'].lower() or 'experience' or 'andhra' in data['name'].lower() in data['name'].lower() or 'skills' in data['name'].lower() or 'education' in data['name'].lower() or 'linkedin' in data['name'].lower() or 'email' in data['name'].lower() or 'developer' in data['name'].lower() or 'resume' in data['name'].lower() or 'professional' in data['name'].lower() or 'java' in data['name'].lower() or 'email' in data['name'].lower() or 'mobile' in data['name'].lower():
            name = extract_name(resume_text)

        else:
            name = data['name']
            nlp_text = nlp(name)
            pattern = [{'POS': 'PROPN'}]

            matcher.add('NAME', None, pattern)

            matches = matcher(nlp_text)
            names = []
            for match_id, start, end in matches:
                span = nlp_text[start:end]
                names.append(span.text)
            if len(names)==0:
                name = extract_name(resume_text)
        if len(name.split()) > 5:
            temp_text = resume_text
            temp_list = resume_text.split("\n")
            temp_text = temp_list[0].replace("  ","-")
            temp_text = temp_text.replace(" ","")
            temp_text = temp_text.replace("-"," ")
            name = temp_text
        if len(name)<=1:
            try:
                name = resume_text.split()
                name = " ".join(name[:2])
            except:
                name = resume_text[:30]
        split_names = name.split(" ")
        try:
            if len(split_names[0])==1 or len(split_names[1])==1:
                name = ".".join(split_names[:2])
        except:
            name = " ".join(split_names[:2])
        #
        number = extract_phone_number(resume_text)
        email = extract_email(resume_text)
        linkedin_links = extract_linkdin_links(resume_text)
        skill_set = extract_skills(resume_text)
        experience = extract_experience(resume_text)
        job_skills = experience_skills(resume_text,experience)
        company = get_company(resume_text,experience)
        gender = extract_gender(resume_text)
        nationality = extract_Nationality(resume_text)
        education = extract_education(resume_text)
        marital_status = extract_status(resume_text)
        location = extract_location(resume_text)
        print("location: "+location)
        if data['university']==[]:
            found_institution = get_institution(resume_text,True)
        else:
            found_institution = get_institution(resume_text, False)
        graduation_year = get_graduation(resume_text,education[1])
        projects = extract_projects(resume_text)
        if data['university']!= []:
            for i in data['university']:
                found_institution.append(i.title())
            found_institution  = list(set(found_institution))
        print(resume_text)
        degree = extract_stream(resume_text,education[0])
        json_dict = {"file_name":file_name,
                     "name":name,"contact_number":number,"email":email,'linkedIn-link':linkedin_links[0],"gender":gender,"nationality":nationality,"marital status":marital_status,
                     "skills":skill_set,"degree":[{"education":filter_education(education[0]),'stream':education[1],"institution":found_institution,
                     "graduation_year":graduation_year[0],"CGPA":graduation_year[1]}],
                     "experience":company,'job skills': job_skills,
                     "projects":projects[0],"github_links":projects[1],"location": location, "word_count": word_count,"bestFit": False, "goodFit": 0}
        return json_dict

        #json_file = json.dumps(json_dict)
        # out_file = open('parsed/'+file_name+".json", "w")

        # json_file = json.dump(json_dict, out_file, indent=6)

        # print(filter_education(education[0]))