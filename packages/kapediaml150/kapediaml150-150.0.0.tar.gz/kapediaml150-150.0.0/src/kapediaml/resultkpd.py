import os
import json
import re
import pathlib
import pickle
import numpy as np
import itertools
import fitz
from PIL import Image
from fuzzywuzzy import fuzz
from paddleocr import PaddleOCR


class Questionsep:
    """
    This class seperate the questions from unstructured ocr output.
    """
    def __init__(self,absolutepath):
        self.model_file = "ocrmodel"
        self.img_path = "images"
        self.input_json = "inputraw.json"
        self.file_input = absolutepath
        self.ocroutput = []
        self.heading_part = []
        self.university = []
        self.level = []
        self.programme = []
        self.subject = []
        self.semester = []
        self.year = []
        self.body_part = []
        self.body_part1 = []
        self.numbers_list  = []
        self.inference_result = []
        self.final_result = []
        self.script_dir = pathlib.Path(__file__).parent.absolute()
        self.files_dir= os.path.join(self.script_dir, self.file_input)
        self.model_file = os.path.join(self.script_dir, self.model_file)
        self.inputjson = os.path.join(self.script_dir,self.input_json)
        self.model = pickle.load(open(self.model_file ,"rb"))

        #import raw data from inputraw.json file and used in whole class
        with open(self.inputjson, "r") as read_jsonfile:
            data= json.load(read_jsonfile)
        self.hbsepration = data["hbsepration"]
        self.univ_list = data["univ_list"]
        self.level_list = data["level_list"]
        self.programme_list = data["programme_list"]
        self.sub_list = data["sub_list"]
        self.semester_list = data["semester_list"]
        self.year_list = data["year_list"]
        self.clean_bodypart = data["clean_bodypart"]
        self.remove_marks = data["remove_marks"]
        self.num_list = data["num_list"]


    def ocr_output(self):
        ocrdata = []
        try:
            for i in range(10):
                doc = fitz.open(self.files_dir)
                page = doc.load_page(i)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                numpy_images = np.asarray(img)

                ocr = PaddleOCR(use_angle_cls=True, lang='en', enable_mkldnn=True )
                result = ocr.ocr(numpy_images, cls=True)
                txts = [line[1][0] for line in result]
                ocrdata.append(txts)
                self.ocroutput = list(np.concatenate(ocrdata))
        except ValueError:
            pass
        return self.ocroutput

    def heading_body(self):
        self.heading_part = []
        self.body_part = []
        for i, line in enumerate(self.ocroutput):
            if line.startswith(tuple(self.hbsepration)):
                self.body_part.clear()
                for j in self.ocroutput[i:]:
                     self.body_part.append(j)
                break
            else:
                self.heading_part.append(line)
                self.body_part.append(line)

        return self.heading_part

    def university_name(self):
        self.university = []
        for i, j in itertools.product(self.univ_list, self.heading_part):
            ratio = fuzz.ratio(i, j.upper())
            if ratio > 80:
                self.university.clear()
                self.university.append(i)
                break

            else:
                self.university = ["Not Found"]

        return self.university

    def exam_level(self):
        self.level = []
        for i, j in itertools.product(self.level_list, self.heading_part):

            x = (j.split(':'))
            x = (x[-1].split('-'))
            x = x[-1]
            ratio = fuzz.ratio(i, x)
            if ratio > 70:
                self.level.clear()
                self.level.append(i)
                break

            if j.startswith(("Level")):
                x = (j.split(':'))
                x = (x[-1].split('-'))
                check = ['']
                x = (x[-1].split(' '))
                if x[0]  in check:
                    x.pop(0)
                    x = ' '.join(x)
                    self.level.clear()
                    self.level.append(x)
                    break

            else:
                self.level =["Not Found"]

        return self.level

    def exam_programme(self):
        self.programme = []
        for i, j in itertools.product(self.programme_list, self.heading_part):

            x = (j.split('/'))
            x = x[0]
            ratio = fuzz.ratio(i, x)
            if ratio > 70:
                self.programme.clear()
                self.programme.append(i)
                break

            if j.startswith(("Programme","Program")):
                x = (j.split(':'))
                x = (x[-1].split('-'))
                check = ['']
                x = (x[-1].split(' '))
                if x[0]  in check:
                    x.pop(0)
                    x = ' '.join(x)
                    self.programme.clear()
                    self.programme.append(x)
                    break

            else:
                self.programme=["Not Found"]

        return self.programme

    def subject_name(self):
        self.subject = []
        for i, j in itertools.product(self.sub_list, self.heading_part):

            x = (j.split(':'))
            x = (x[-1].split('-'))
            x = x[-1]
            ratio = fuzz.ratio(i, x)
            if ratio > 70:
                self.subject.clear()
                self.subject.append(i)
                break

            if j.startswith(("Subject","Course")):
                x = (j.split(':'))
                x = (x[-1].split('-'))
                check = ['']
                x = (x[-1].split(' '))
                if x[0]  in check:
                    x.pop(0)
                    x = ' '.join(x)
                    self.subject.clear()
                    self.subject.append(x)
                    break

            else:
                self.subject =["Not Found"]

        return self.subject

    def exam_semester(self):
        self.semester = []
        for i, j in itertools.product(self.semester_list, self.heading_part):

            ratio = fuzz.ratio(i, j)
            if ratio > 70:
                self.semester.clear()
                self.semester.append(i)
                break

            if j.startswith(("Semester")):
                x = (j.split(':'))
                x = (x[-1].split('-'))
                check = ['']
                x = (x[-1].split(' '))
                if x[0]  in check:
                    x.pop(0)
                    x = ' '.join(x)
                    self.semester.clear()
                    self.semester.append(x)
                    break

            x = (j.split('/'))
            try:
                x = x[1]
                ratio = fuzz.ratio(i, x)
                if ratio > 70:
                    self.semester.clear()
                    self.semester.append(i)
                    break
            except IndexError:
                pass

            else:
                self.semester =["Not Found"]

        return self.semester

    def exam_year(self):
        self.year = []
        for i, j in itertools.product(self.year_list, self.heading_part):

            x = (j.split(' '))
            x = x[0]
            ratio = fuzz.ratio(i, x)
            if ratio > 90:
                self.year.clear()
                self.year.append(i)
                break

            else:
                self.year =["Not Found"]

        return self.year

    def body_cleaning(self):
        body_part1  = []
        for line in self.body_part:
            re_result = re.sub(r"^[[{*][0-9].*|^[(][0-9].*|^[0-9][.+x=][0-9][^a-z].*"," ",line)
            if not re_result.startswith(tuple(self.clean_bodypart)):
                body_part1.append(re_result)
            else:
                pass
        self.body_part1 = [x for x in  body_part1 if x not in self.remove_marks]

        return self.body_part1


    def start_with_num(self,line):
        x = (line.split(' '))
        y = (x[0].split('.'))
        if y[0] not in self.num_list:
            start_with_num = 0
        else:
            start_with_num = 1
        return start_with_num

    def check_new_line(self,line,next_line):

        i = self.start_with_num(line)
        j = self.start_with_num(next_line)
        if i == 0 and j == 1:
            check_new_line = 0
        elif i == 1 and j == 1:
            check_new_line = 0
        else:
            check_new_line = 1

        return check_new_line

    def  end_with_fullstop_questionmark(self,line):

        fullstop_qtionmrk = [ ".", "?"]
        x = (list(line[-1]))
        if x[-1] in fullstop_qtionmrk:
            end_with_fullstop_questionmark = 0
        else:
            end_with_fullstop_questionmark = 1

        return end_with_fullstop_questionmark

    def space_count(self,line):
        new_str, count = re.subn(r'\s', ' ', line)
        space_count = count

        return space_count

    def inference(self):
        self.inference_result = []
        temp = []
        for index,line in enumerate(self.body_part1):

            f1 = self.start_with_num(line)
            try:
                f2 = self.check_new_line(line, self.body_part1[index+1])
            except IndexError:
                f2 = 0
            f3 = self.end_with_fullstop_questionmark(line)
            f4 = self.space_count(line)
            one_line_features = np.array([[f1,f2,f3,f4]])

            model_prediction = self.model.predict(one_line_features)

            if model_prediction ==1:
                temp.append(line)
            if model_prediction ==0:
                temp.append(line)
                self.inference_result.append(temp)
                temp = []
            else:
                pass
        return self.inference_result

    def post_processing(self):
        final_list1 = []
        for line in self.inference_result:
            x = len([w for s in line for w in re.findall(r'\s', s)])
            if x > 1:
                concat= ' '.join(line)
                final_list1.append(concat)
            else:
                pass

        final_list2 = []
        num_list1 = self.num_list[0:204]
        for line in final_list1:
            x = line.split(' ')
            y = (x[0].split('.'))
            if y[0] in num_list1:
                z = line.replace(y[0],'')
                final_list2.append(z)
            else:
                final_list2.append(line)

        final_list3 = []
        check = ['', '.']
        for line in final_list2:
            x = line.split(' ')
            if x[0]  in check:
                x.pop(0)
                concat = ' '.join(x)
                final_list3.append(concat)
            else:
                final_list3.append(line)

        final_list4 = []
        for line in final_list3:
            x = line.split(')')
            if x[0]  in num_list1:
                x.pop(0)
                concat = ' '.join(x)
                final_list4.append(concat)
            else:
                final_list4.append(line)

        check = ['', '.']
        self.final_result = []
        for line in final_list4:
            x = line.split(' ')
            if x[0]  in check:
                x.pop(0)
                concat = ' '.join(x)
                self.final_result.append(concat)
            else:
                self.final_result.append(line)
        return self.final_result

    def final_function(self):
        ocr_result= self.ocr_output()
        heading_result  = self.heading_body()
        university = self.university_name()
        level = self.exam_level()
        programme = self.exam_programme()
        subject    = self.subject_name()
        semesters = self.exam_semester()
        years     = self.exam_year()
        bodypart_clening = self.body_cleaning()
        inference_result = self.inference()
        final_result = self.post_processing()

        # data = {'University':university ,'Level':level,'Programe':programme,'Subject':subject,
        #         'Semesters':semesters ,'years':years,'Questions':final_result}
        # json_object = json.dumps(data, indent = 4)

        # with open('output.json', 'w') as write_file:
        #     write_file.write(json_object)

        return {"university": university ,
                "Level": level,
                "Program": programme,
                "Subject": subject ,
                "Semester":semesters,
                "Years":years ,
                "Questions":final_result}

# questiosep = Questionsep("/home/tapendra/Desktop/pypi-package/images/img1.png")
# final_output = questiosep.final_function()
# print(final_output)
# t2 = time.monotonic()
# print("time test",(t2-t1))
# if __name__ == '__main__':
#     questiosep = Questionsep()
#     ocr_result= questiosep.ocr_output()
#     heading_result  = questiosep.heading_body()
#     university = questiosep.university_name()
#     subject    = questiosep.subject_name()
#     bodypart_clening = questiosep.body_cleaning()
#     inference_result = questiosep.inference()
#     final_result = questiosep.post_processing()

#     data = {'University':university ,'Subject':subject,'Questions':final_result}
#     json_object = json.dumps(data, indent = 4)

#     with open('output.json', 'w') as write_file:
#         write_file.write(json_object)
