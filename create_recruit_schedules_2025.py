import sys
import subprocess
import math
import pandas as pd
import numpy as np
import platform

#TO DO:
    #Add GPP contingency
    #Change location of "interview" schedule
    #Format for printing

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


def print_interview_table(outfile, header, slot_times, names, slot_location):

    title = f"""<br><h3><center>{header}</center></h3>"""
    outfile.write(title)

    header = """\
<table style="font-family:arial;">
  <tr>
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#5D7B9D"><font color="#fff">Time</font></th> 
   <th style="text-align:center; font-size:120%" width=50%" bgcolor="#5D7B9D"><font color="#fff">Interview</font></th>   
   <th style="text-align:center; font-size:120%" width=25%" bgcolor="#5D7B9D"><font color="#fff">Location</font></th>
   
  </tr>
"""
    outfile.write(header)

    colors = ["white", "light-gray"]
    for i in range(len(slot_times)):
        color = colors[i%2]
        rowtext = f"""\
<tr style="background-color:{color}">
 <td style="text-align:center" width=25%>{slot_times[i]}</td>
"""
        outfile.write(rowtext)
        rowtext = f"""\
 <td style="text-align:center" width=25%>{names[i]}</td>
"""
        outfile.write(rowtext)
        
        rowtext = f"""<td style="text-align:center" width=50%>{slot_location[i]}</td></tr>"""

    
        outfile.write(rowtext)
    outfile.write("</table>")
    



def print_extras(outfile):
    t = f"""\



<br>
<center>
<h3>Thursday, February 13</h3>
</center>

<table style="font-family:arial;">
  <tr>
   <th colspan="3" style="text-align:center; font-size:150%" bgcolor="#e5b8b7"><font color="#000"></font></th>
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
<h3>Friday, February 14 </h3>
</center>

<table style="font-family:arial;">
  <tr>
   <th colspan="3" style="text-align:center; font-size:150%" bgcolor="#e5b8b7"><font color="#000"></font></th>
  </tr>
</table>

<div style="page-break-before:always;">



<br>
<center>
<h3>Saturday, February 15</h3>
</center>

<table style="font-family:arial;">
  <tr>
  <th colspan="3" style="text-align:center; font-size:150%" bgcolor="#e5b8b7"><font color="#000"></font></th>
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
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> All day </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF">  <strong> Departures </strong>  </td>
  <td style="text-align:center; font-size:100%" width=25%" bgcolor="#FFFFFF"> You can depart from the hotel at any point after check-out, when you are ready to leave. You can arrange your own transportation and be reimbursed for your Uber or taxi. </td>
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

def load_interview_data(filename='./Appl_Fac Interviews_2025.xlsx'):
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

    interviews = interviews.T #Transpose interview matrix table to make applicants column headers
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
            
#######

        #Find non-empty interview slots for recruit r
        interview_slots = interviews.loc[:,r].values
        interviewers = interviews.loc[interview_slots>0].index.values
        interview_slots = interview_slots[interview_slots>0].astype(int)

        times = []
        location = []
        names = []
        time_slot = []
        text1 = "Optional tours"
        text2 = "Meet in SFH 3rd floor lobby"

        #For each interview, pull relevant interviewer data
        if len(interview_slots):
            htmlfile = f"./html/applicants/{r}_Brown_Schedule.html"
            pdffile = htmlfile.replace("html","pdf")
            with open(htmlfile, "w") as outfile:
                for i in slots.index:
                    time_slot.append(i)
                    if i in interview_slots:
                        if (interview_slots==i).sum() != 1:
                            print("Error!");
                        else:
                            interviewer = interviewers[interview_slots==i][0]
                            times.append(slots.loc[i]["Time"])
                            f = faculty.loc[interviewer]
                            location.append(f["RoomID"])
                            if interviewer in current_students.index:
                                names.append("Graduate Student Interview: " + f["FacultyFirst"]+ " " + interviewer)
                            else:
                                names.append("Faculty Interview: "+ f["FacultyFirst"] + " " + interviewer)
                    if i not in interview_slots: #If no interview, append info for optional tours
                        times.append(slots.loc[i]["Time"]) 
                        names.append(text1)
                        location.append(text2)
                
                #Append events that are the same for every itinerary
                times.append("12:00pm - 12:55pm")
                names.append("Lunch")
                time_slot.append(141200)
                location.append("SFH 3rd floor lobby")
                
                times.append("9:00am - 10:00am")
                names.append("Welcome meeting")
                time_slot.append(140900)
                location.append("Peterutti Lounge")
                
                times.append("10:00am - 10:55am")
                names.append("Faculty Data Blitz")
                time_slot.append(141000)
                location.append("Peterutti Lounge")
 
                #Sort all variables by time slot ID so they are in order of time
                sorted_pairs = sorted(zip(time_slot, times, names, location))
                times_sorted = [v2 for v1, v2, v3, v4 in sorted_pairs]
                names_sorted = [v3 for v1, v2, v3, v4 in sorted_pairs]
                location_sorted = [v4 for v1, v2, v3, v4 in sorted_pairs]
                                    
                            
                outfile.write(opening.format(recruit_goesby=recruit_goesby, recruit_last=recruit_last))
                outfile.write(style)
                outfile.write(body1.format(recruit_goesby=recruit_goesby, recruit_last=recruit_last, recruit_itinerary=recruit_itinerary,host_last=recruit_host_last, host_first=recruit_host_goesby))
                print_interview_table(outfile, "Interviews (Friday, February 14)", times_sorted, names_sorted, location_sorted)
            
#######
                
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