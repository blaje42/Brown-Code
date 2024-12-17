import sys
import subprocess
import platform

import pandas as pd
import numpy as np

opening = r"""
<!DOCTYPE html>  
<html lang="US">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <title>{faculty_last} Schedule</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
"""

body1 = r"""
  </head>
<body class="normal">
  <div id="wrapper">


<center>
<h2>
Neuro Grad Interviews 2025
</h3>
</center>


<center>
<h3>
{faculty_last} | {faculty_room}  
<br>
<br> 
<a href="{faculty_itinerary}" target="_blank">Update Schedule</a>
</h3>
</center>
"""


def print_interview_table(outfile, slot_dates, slot_times, names, pdflinks, zoom_link,
                          first_names, last_names, start_times, stop_times, form_names):
    header = """\
<table>
  <tr>
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#5D7B9D"><font color="#fff">Time</font></th>
   <th style="text-align:center; font-size:120%" width=30%" bgcolor="#5D7B9D"><font color="#fff">Applicant (Click for Link)</font></th>
   <th style="text-align:center; font-size:120%" width=10%" bgcolor="#5D7B9D"><font color="#fff">Calendar</font></th>
   <th style="text-align:center; font-size:120%" width=10%" bgcolor="#5D7B9D"><font color="#fff">Eval</font></th>
  </tr>
"""
    outfile.write(header)

    colors = ["white", "light-gray"]
    for i in range(len(slot_dates)):
        applicant_last = last_names[i]
        applicant_first = first_names[i]
        day_of_month = day_of_months[i]
        start_time = start_times[i]
        stop_time = stop_times[i]
        application_link = pdflinks[i].replace('#','')

        add_to_gcal_href = f"https://calendar.google.com/calendar/u/0/r/eventedit?text=Neuro+Grad+Interview+[{applicant_first}+{applicant_last}]&dates=202502{day_of_month}T{start_time}/202502{day_of_month}T{stop_time}&details=Application:+{application_link}+<br><br>+Schedule:+{faculty_itinerary}&location={faculty_room}&sf=true&output=xml"
        eval_href = f"https://docs.google.com/forms/d/e/1FAIpQLScFvnL1nvZmvVFQuq_zPjV2c4qG8rnGvDEshoitImiS5OpzBQ/viewform?usp=sf_link+usp=pp_url&entry.360103649={form_names[i]}"
    
        color = colors[i%2]
        rowtext = f"""\
<tr style="background-color:{color}">
 <td style="text-align:center" width=25%>{slot_times[i]}</td>
 <td style="text-align:center" width=30%><a href="{pdflinks[i]}" target="_blank">{names[i]}</a></td>
 <td style="text-align:center" width=10%><a href="{add_to_gcal_href}" target="_blank">Add</a></td>
  <td style="text-align:center" width=10%> <a href="{eval_href}" target="_blank">Form</a></td>
</tr>
"""
        outfile.write(rowtext)
    outfile.write("</table>")



body2 = r"""



<center><h4>
<p><a href="https://docs.google.com/forms/d/e/1FAIpQLScFvnL1nvZmvVFQuq_zPjV2c4qG8rnGvDEshoitImiS5OpzBQ/viewform?usp=sf_link" target="_blank">Blank NSGP/GPP Evaluation Form</a></p>
</h4></center>


<br>

<center><h3>
Contacts 
</h3></center>
<center>
<a href="mailto:carol_viveiros@brown.edu">Carol Viveiros</a> / 508-989-3873  &nbsp | &nbsp
<a href="mailto:jennifer_blackwell@brown.edu">Jennifer Blackwell</a> /  401-863-1693
</center>

<!-- ##END MARKED WRAPPER## -->
    </div>
</body>
</html>
"""


def load_interview_data(filename='./Appl_Fac Interviews_2024.xlsx'):
    slots = pd.read_excel(filename, sheet_name="InterviewSlots",
                      index_col=0, dtype={'a': int})
    faculty = pd.read_excel(filename,sheet_name="FacultyInfo", index_col=0)
    students = pd.read_excel(filename,sheet_name="StudentInfo", index_col=0)
    interviews = pd.read_excel(filename,sheet_name="InterviewMatrix",index_col=0)
    forminfo = pd.read_excel(filename, sheet_name="FormInfo", index_col=0)
    current_students = pd.read_excel(filename, sheet_name="CurrentStudents", index_col=0)
    return students, faculty, interviews, slots, forminfo, current_students


def do_cmd(cmd, verbose=False, execute=True):
    if verbose:
        print(cmd)
    if execute:
        ret = subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    students, faculty, interviews, slots, forminfo, current_students = load_interview_data()

    with open("./schedule_style.dat") as s:
        style = s.read()
    
    for f in interviews.columns:
        faculty_last = f
        last_name = f

        faculty_last = last_name
        faculty_room = faculty.loc[f]["RoomID"]
        faculty_itinerary = faculty.loc[f]["Itinerary"]
        new_slots = interviews.loc[:,f].values
        recruits = interviews.loc[new_slots>0].index.values
        new_slots = new_slots[new_slots>0].astype(int)

        times = []
        dates = []
        names = []
        days = []
        pdflinks = []
        applicants = []
        last_names = []
        first_names = []
        day_of_months = []
        start_times = []
        stop_times = []
        form_names = []

        if len(new_slots):
            htmlfile = f"./html/faculty/{f}_Schedule.html"
            pdffile = htmlfile.replace("html","pdf")
            with open(htmlfile, "w") as outfile:
                for i in slots.index:
                    if i in new_slots:
                        applicant_name = recruits[new_slots == i][0]
                        applicant_first = students.FirstName[applicant_name]
                        applicant_last = students.LastName[applicant_name]
                        form_names.append(forminfo.FormEntry[applicant_name])
                        d = slots.loc[i]["Date"]
                        t_start, t_stop = slots.loc[i]["Time"].split('-')
                        start_timestamp = pd.Timestamp(f"2025-02-{d.day}-{t_start}")
                        stop_timestamp = pd.Timestamp(f"2025-02-{d.day}-{t_stop}")
                        times.append(slots.loc[i]["Time"])
                        dates.append(d.date())
                        days.append(f"{d.day_name()}, {d.month_name()} {d.day}")
                        applicants.append(f"{applicant_first} {applicant_last}")
                        day_of_months.append(d.day)
                        #start_times.append(f"{start_timestamp.hour*100+start_timestamp.minute:04d}")
                        #stop_times.append(f"{stop_timestamp.hour*100+stop_timestamp.minute:04d}")
                        if start_timestamp.minute == 0:
                            start_times.append(f"{(start_timestamp.hour-1)*100+55:04d}")
                        else:
                            start_times.append(f"{start_timestamp.hour*100+start_timestamp.minute-5:04d}")

                        if stop_timestamp.minute == 0:
                            stop_times.append(f"{(stop_timestamp.hour-1)*100+55:04d}")
                        else:
                            stop_times.append(f"{stop_timestamp.hour*100+stop_timestamp.minute-5:04d}")
                        
                        last_names.append(applicant_last)
                        first_names.append(applicant_first)
                        r = students.loc[applicant_name]
                        names.append(r["GoesBy"]+" "+applicant_last +
                                     " ("+r["Program"].replace(" ", "/")+")")

                        # Different links for grad students and faculty
                        if f not in current_students.index:
                            pdflinks.append(r["GDriveLink"])
                            qa_session_link = "https://brown.zoom.us/j/98599320764?pwd=bytPMlVwY1E4SVcxY212aGtaSmROQT09"

                        else:
                            pdflinks.append(r["CV"])
                            qa_session_link = "https://brown.zoom.us/j/94523182899?pwd=a1QxRE1JbEtSSXB4K2JMQlBXT3A3dz09"

                outfile.write(opening.format(faculty_last=faculty_last))
                outfile.write(style)
                outfile.write(body1.format(faculty_last=faculty_last, faculty_room=faculty_room, faculty_itinerary=faculty_itinerary))
                print_interview_table(outfile, days, times, names, pdflinks, faculty_room, 
                                      first_names, last_names, start_times, stop_times, form_names)
                outfile.write(body2.format(qa_session_link=qa_session_link))
                
                if platform.system() == "Windows":
                    converter = "wkhtmltopdf.exe"
                else:
                    converter = "/usr/local/bin/wkhtmltopdf"
                cmd = f"{converter} --page-size Letter \"{htmlfile}\" \"{pdffile}\""
                do_cmd(cmd, verbose=True, execute=False)
                
# In command prompt:
    #cd to folder containing script then:
    #python create_recruit_schedules.py>create.bat
    #create
