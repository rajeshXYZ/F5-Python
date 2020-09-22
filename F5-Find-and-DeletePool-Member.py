My codes
-------

F5-VLAN-PRUNING USING PYTHON

#!/usr/bin/python
import subprocess
import sys
#Function find whether this UNIT is active or standby using the command 'tmsh list sys db failover.state'
def find_unit_state():
  u_state  = subprocess.Popen(['tmsh','list','sys','db','failover.state'],stdout=subprocess.PIPE)
  us_output = u_state.communicate()[0]
  get_unit_state = us_output.split()[5]
  if "active" not in get_unit_state:
      print "!!! This F5 is not an active unit. Hence I am exiting. Please execute this script from an active F5 unit !!!"
      sys.exit()
  else:
      print "\n*** This F5 Unit is Active. Hence proceeding to the next step ***"

#Function to open the a file which contains pool info pasted from ticket and then get you the tmsh command list for you to verify and then copy 
#and paste. This hopefully should save you time
def list_tmsh_cmd():
  myfile = open("f5pools.txt","r")
  print "*** LISTING THE COMMAND TO DELETE THE POOL MEMBERS LISTED IN THE FILE ***\n"
  for eachline in myfile:
    fields = eachline.replace(',','')
    split = fields.split()
    x = split[2]
    y = split[6]
    proto1 = subprocess.Popen(['tmsh','list','ltm','pool',x],stdout=subprocess.PIPE)
    output = proto1.communicate()[0]
    newoutput = output.split()
    for word in newoutput:
       if y in word:
         members  = word.replace(':',' ')
         find_protocol = members.split()
         found_protocol = find_protocol[1]
         print  "tmsh modify ltm pool " + x + " members delete { " + y +":"+found_protocol+ "}"

def main():
    find_unit_state()
    list_tmsh_cmd()

main()
 
 
