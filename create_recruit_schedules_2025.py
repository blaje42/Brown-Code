import sys
import subprocess
import math
import pandas as pd
import numpy as np
import platform

opening = r"""
<!DOCTYPE html>  
<html lang="US">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <title>{recruit_goesby} {recruit_last} Schedule</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
"""

body1 = r"""
  </head>
<body class="normal">
  <div id="wrapper">


<center>
<h2>
Brown University NSGP & GPP Interviews 2025
</h3>
</center>

<center>
<h3>
<a href="{recruit_itinerary}" target="_blank">{recruit_goesby} {recruit_last}</a>   
</h3>
</center>

<center>
<h3>
Your host: {host_first} {host_last}
</h3>
</center>
"""


def print_interview_table(outfile, header, slot_dates, slot_times, names):

    title = f"""<br><h3><center>{header}</center></h3>"""
    outfile.write(title)

    header = """\
<table>
  <tr>
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#5D7B9D"><font color="#fff">Time</font></th> 
   <th style="text-align:center; font-size:120%" width=50%" bgcolor="#5D7B9D"><font color="#fff">Interview</font></th>   
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#5D7B9D"><font color="#fff">Location</font></th>
   
  </tr>
"""
    outfile.write(header)

    colors = ["white", "light-gray"]
    for i in range(len(slot_dates)):
        color = colors[i%2]
        rowtext = f"""\
<tr style="background-color:{color}">
 <td style="text-align:center" width=25%>{slot_dates[i]}</td>
"""
        outfile.write(rowtext)
        rowtext = f"""\
 <td style="text-align:center" width=25%>{slot_times[i]}</td>
"""
        outfile.write(rowtext)
        
        rowtext = f"""<td style="text-align:center" width=50%>{names[i]}</td></tr>"""

 #       if zoomlinks[i] != "":
 #           rowtext = f"""<td style="text-align:center" width=50%><a href="{zoomlinks[i]}" target="_blank">{names[i]}</a></td></tr>"""
 #       else:
 #           rowtext = f"""<td style="text-align:center" width=50%>{names[i]}</td></tr>"""
    
        outfile.write(rowtext)
    outfile.write("</table>")
    



def print_extras(outfile):
    t = f"""\



<br>
<center>
<h3>Thursday, February 13 </h3>
</center>

<table>
  <tr>
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#e5b8b7"><font color="#000">Time</font></th>
   <th style="text-align:center; font-size:120%" width=50%" bgcolor="#e5b8b7"><font color="#000">Event</font></th>
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#e5b8b7"><font color="#000">Location</font></th>
  </tr>
  
  <tbody>
  <tr>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> 1:00pm - 5:00pm  </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> <strong> Arrival </strong> </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> Hampton Inn & Suites Providence Downtown <br> <em> 58 Weybosset St. <br> Providence, RI <br> 401-608-3500 </em>  </td>
  </tr>
  <tr>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> 3:00pm - 6:00pm  </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> <strong> Meet current students </strong> in the hotel lobby and collect welcome bags, including your itinerary  </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> Hampton Inn & Suites Providence Downtown </td>
  </tr>
  <tr>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> 5:45pm & 6:15pm  </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> <strong> Transportation to dinner - shuttle service </strong> </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> Meet in hotel lobby </td>
  </tr>
  <tr>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> 6:00pm - 8:30pm  </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> <strong> Dinner with students and faculty (casual) </strong> </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> Flatbread <br> <em> 161 Cushing St. <br> Providence, RI </em> </td>
  </tr>
  <tr>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> 8:00pm & 8:30pm  </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> <strong> Transportation to hotel - shuttle service </strong> </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> Flatbread </td>
  </tr>

  </tbody>
  </table>
  



<br>
<center>
<h3>Friday, February 14 (Morning) </h3>
</center>

<table>
  <tr>
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#e5b8b7"><font color="#000">Time</font></th>
   <th style="text-align:center; font-size:120%" width=50%" bgcolor="#e5b8b7"><font color="#000">Event</font></th>
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#e5b8b7"><font color="#000">Location</font></th>
  </tr>
</table>

<div style="page-break-before:always;">

<center>
<h3>Friday, February 14 (Afternoon) </h3>
</center>

<table>
  <tr>
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#e5b8b7"><font color="#000">Time</font></th>
   <th style="text-align:center; font-size:120%" width=50%" bgcolor="#e5b8b7"><font color="#000">Event</font></th>
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#e5b8b7"><font color="#000">Location</font></th>
  </tr>
</table>

<br>
<center>
<h3>Saturday, February 15</h3>
</center>

<table>
  <tr>
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#e5b8b7"><font color="#000">Time</font></th>
   <th style="text-align:center; font-size:120%" width=50%" bgcolor="#e5b8b7"><font color="#000">Event</font></th>
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#e5b8b7"><font color="#000">Location</font></th>
  </tr>
  <tr>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> 9:00am - 12:00pm  </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> <strong> Group brunches </strong>  </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> Check with your host for more details </td>
  </tr>
  <tr>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> 10:00am - 12:00pm  </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> <strong> Neighborhood/Apartment tours </strong>  </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> Check with your host for more details </td>
  </tr>
  <tr>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> <strong> Departures </strong> </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> You can depart from the hotel at any point after check-out, when you are ready to leave. You can arrange your own transportation and be reimbursed for your Uber or taxi.   </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF">  </td>
  </tr>
</table>


<br>
</div>

"""
    outfile.write(t)
# Want the following: (1) For possible interview slots - if interview time_slot is empty then text is "Optional Tours or Panels" and also hard code lunch in the middle of a table?
# (2) Have a GPP case for a specific time slot that will be their group meeting
body2 = """\

<br>
<br>
<center><h3>
Contacts 
</h3></center>

<center>
<span style="font-size:130%">Your Host: <a href="mailto:{host_email}">{host_first} {host_last}</a></span>
</center>

<center>
<a href="mailto:carol_viveiros@brown.edu">Carol Viveiros</a> / 508-989-3873  &nbsp | &nbsp
<a href="mailto:jennifer_blackwell@brown.edu">Jennifer Blackwell</a> /  401-863-1693
</center>

<!-- ##END MARKED WRAPPER## -->
    </div>
</body>
</html>
"""

#body3, if there are 2 hosts...
body3 = """\

<center><h3>
Contacts
</h3></center>

<center>
<span style="font-size:130%">Your Hosts: <a href="mailto:{host_email}">{host_first} {host_last}</a> and <a href="mailto:{host_email2}">{host_first2} {host_last2}</a></span>
</center>

<br>
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
    current_students = pd.read_excel(
        filename, sheet_name="CurrentStudents", index_col=0)
    interviews = pd.read_excel(filename,sheet_name="InterviewMatrix",index_col=0)
    return students, current_students, faculty, interviews, slots


def do_cmd(cmd, verbose=False, execute=True):
    if verbose:
        print(cmd)
    if execute:
        ret = subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    students, current_students, faculty, interviews, slots = load_interview_data()

    with open("./schedule_style.dat") as s:
        style = s.read()

    interviews = interviews.T
    for r in interviews.columns:
        recruit_last = students.loc[r]["LastName"]
        recruit_goesby = students.loc[r]["GoesBy"]
        recruit_itinerary = "https://www.brown.edu/academics/neuroscience/graduate/"
        recruit_host_last = students.loc[r]["HostLast"]
        recruit_program = students.loc[r]["Program"]
        recruit_host_goesby = current_students.loc[recruit_host_last]["GoesBy"]
        recruit_host_email = current_students.loc[recruit_host_last]["Email"]

        # Check if there's a second host
        recruit_host_last2 = students.loc[r]["HostLast2"]
        if type(recruit_host_last2) != str: recruit_host_last2 = None
        if recruit_host_last2:
            recruit_host_goesby2 = current_students.loc[recruit_host_last2]["GoesBy"]
            recruit_host_email2 = current_students.loc[recruit_host_last2]["Email"]
        else:
            recruit_host_goesby2, recruit_host_email2 = None, None

        new_slots = interviews.loc[:,r].values
        interviewers = interviews.loc[new_slots>0].index.values
        new_slots = new_slots[new_slots>0].astype(int)

        times = []
        location = []
        names = []
        zoomlinks = []

        if len(new_slots):
            htmlfile = f"./html/applicants/{r}_Brown_Schedule.html"
            pdffile = htmlfile.replace("html","pdf")
            with open(htmlfile, "w") as outfile:
                hours = [800, 830, 900, 930, 1000, 1030, 1100, 1130, 1300, 1330, 1400, 1430, 1500, 1530, 1600, 1630]
                for daycode in [180000, 190000, 220000, 230000]:
                    for i in [h+daycode for h in hours]:
                        if i in new_slots:
                            if (new_slots==i).sum() != 1:
                                print("Error!");
                            else:
                                interviewer = interviewers[new_slots==i][0]
                                times.append(slots.loc[i]["Time"])                             
                                f = faculty.loc[interviewer]
                                location.append(f["RoomID"])
                                if interviewer in current_students.index:
                                    names.append(f["FacultyFirst"]+ " " + interviewer + " (grad student)")
                                else:
                                    names.append(f["FacultyFirst"] + " " + interviewer)
                            
                outfile.write(opening.format(recruit_goesby=recruit_goesby, recruit_last=recruit_last))
                outfile.write(style)
                outfile.write(body1.format(recruit_goesby=recruit_goesby, recruit_last=recruit_last, recruit_itinerary=recruit_itinerary,host_last=recruit_host_last, host_first=recruit_host_goesby))
                print_interview_table(outfile, "Interviews (Friday, February 14)", times, names, location)
                
                print_extras(outfile)
                if not recruit_host_last2: 
                    outfile.write(body2.format(host_last=recruit_host_last, host_first=recruit_host_goesby, host_email=recruit_host_email))
                else:
                    outfile.write(body3.format(host_last=recruit_host_last, host_first=recruit_host_goesby, host_email=recruit_host_email,
                                               host_last2=recruit_host_last2, host_first2=recruit_host_goesby2, host_email2=recruit_host_email2))

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