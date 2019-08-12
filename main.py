'''
Program works with the way Labview will record the data (50 trials)
Will calculate the magnitude of the electric field used from user input of amps and distance between field.
Does not record error margins for values obtained.
'''
from math import log, pi, exp

def raw_data(filename, R1_list, R2_list, R3_list, R4_list, R5_list, R6_list, R7_list, R8_list, H1_list, H2_list, H3_list, H4_list, H5_list, H6_list, H7_list, H8_list):
  '''
  Turns the .txt/.csv file into lists of measured voltages (V) for each configuration
  :side effect: creates 16 lists (for configurations 1-8 for resitivity and hall measurements) of 100 voltage measurements
  '''
  data_file = open(filename)
  all_lines = data_file.readlines()
  for i in range (len(all_lines)):
    curr_line = all_lines[i].split(",")
  #Compile resitivity meausrements (first 50 lines)
    if i < 50:
      R1_list.append(abs(float(curr_line[0])))
      R2_list.append(abs(float(curr_line[1])))
      R3_list.append(abs(float(curr_line[2])))
      R4_list.append(abs(float(curr_line[3])))
      R5_list.append(abs(float(curr_line[4])))
      R6_list.append(abs(float(curr_line[5])))
      R7_list.append(abs(float(curr_line[6])))
      R8_list.append(abs(float(curr_line[7])))
  #Compile -B field measurements (lines 51-100)
    elif 51 < i < 100:
      H1_list.append(float(curr_line[0]))
      H2_list.append(float(curr_line[1]))
      H3_list.append(float(curr_line[2]))
      H4_list.append(float(curr_line[3]))
    #Compile +B field measurements (lines 101-150)
    else:
      H5_list.append(float(curr_line[0]))
      H6_list.append(float(curr_line[1]))
      H7_list.append(float(curr_line[2]))
      H8_list.append(float(curr_line[3]))
  data_file.close()

def get_average(a_list):
  '''
  :return: average value of a list 
  NOTE: Set as new variable (R0-R8/H0-H8) that is the average voltage for each configuration
  '''
  sum = 0
  for i in range (len(a_list)):
    sum += a_list[i]
  average = sum / (len(a_list))
  return average

def error_check(R1, R2, R3, R4, R5, R6, R7, R8):
  '''
  Uses EQ8 & EQ9 (NIST) to check that error is <5% (preferably <3%)
  :side effect: prints high error warning for the uncertain value(s), or notifies user of minimal uncertainity
  '''
  sum1 = R1 + R5
  sum2 = R2 + R6
  sum3 = R3 + R7
  sum4 = R4 + R8
  p_error1 = abs((sum1-sum3)/sum3) * 100
  p_error2 = abs((sum2-sum4)/sum4) * 100
  p_error3 = abs((R1 - R5)/R1) * 100
  p_error4 = abs((R2 - R6)/R2) * 100
  p_error5 = abs((R3 - R7)/R3) * 100
  p_error6 = abs((R4 - R8)/R4) * 100
  print("\n----- (Percent) Error Checking -----")
  if p_error1 > 5:
    if p_error3 > p_error5:
      print("ATTENTION: (EQ9) Uncertainty in R1/R5:", p_error1)
    else:
      print("ATTENTION: (EQ9) Uncertainty in R3/R7:", p_error1)
  elif p_error1 < 3:
    print("Minimal error", p_error1)
  if p_error2 > 5:
    if p_error4 > p_error6:
      print("ATTENTION: (EQ9) Uncertainty in R2/R6:", p_error2)
    else:
      print("ATTENTION: (EQ9) Uncertainty in R4/R8:", p_error2)
  elif p_error2 < 3:
    print("Minimal error", p_error2)
  if p_error3 > 5:
    print("ATTENTION: Uncertainty in R1/R5:", p_error3)
  elif p_error3 < 3:
    print("Minimal error", p_error3)
  if p_error4 > 5:
    print("ATTENTION: Uncertainty in R2/R6:", p_error4)
  elif p_error4 < 3:
    print("Minimal error", p_error4)
  if p_error5 > 5:
    print("ATTENTION: Uncertainty in R3/R7:", p_error5)
  elif p_error5 < 3:
    print("Minimal error", p_error5)
  if p_error6 > 5:
    print("ATTENTION: Uncertainty in R4/R8:", p_error6)
  elif p_error6 < 3:
    print("Minimal error", p_error6)

def sheet_resistance(R1, R2, R3, R4, R5, R6, R7, R8):
  '''
  Finds the sheet resistance by first finding Ra and Rb
  :return: value of sheet resistance (ohms/square)
  '''
  Ra = (R1 + R5 + R3 + R7) / 4 
  Rb = (R2 + R4 + R6 + R8) / 4
  delta = 0.0005
  zo = 2 * (log(2)) / ((pi) * (Ra + Rb))
  y1 = (1 / exp(pi * zo * Ra)) + (1 / exp(pi * zo * Rb))
  z = zo - ((1-y1)*(pi))/ (((Ra / exp(pi * zo * Ra)) + ((Rb / exp(pi * zo * Rb)))))
  check = (z - zo) / zo
  while check > delta:
    zo = z
    y1 = (1 / exp(pi * zo * Ra)) + (1 / exp(pi * zo * Rb))
    z = zo - ((1-y1)*(pi))/ (((Ra / exp(pi * zo * Ra)) + ((Rb / exp(pi * zo * Rb)))))
    check = (z - zo) / zo
  Rs = 1 / z
  return Rs

def find_resistivity(Rs, d):
  '''
  :param: Rs - sheet resistance
  :param: d - thickness of sample (in nm)
  :return: bulk resitivity (ohm*meter) of the sample
  '''
  p = Rs * d * 10**-7
  return p

def HV(H1, H2, H3, H4, H5, H6, H7, H8):
  '''
  :return: Sum of the voltages measured with positive and negative magnetic fields
  '''
  V_sum = (-H1 - H2 - H3 - H4 + H5 + H6 + H7 + H8)
  return V_sum

def find_type(V_sum):
  if V_sum > 0:
    return "p-type"
  elif V_sum < 0:
    return "n-type"
  else:
    return "both"

def scdensity(current, mag_field, V_sum):
  '''
  Finds the sheet carrier density (cm^-2) of the sample
  '''
  q = 1.602 * (10 **(-19))
  scdensity = ((8 * (10**(-8))) * (current * 10**-9) * mag_field) / (q * V_sum)
  return scdensity

def bcdensity(scdensity, d):
  '''
  Finds the bulk carrier density (cm^-3) of the sample
  '''
  bcdensity = scdensity / (d * 10**-7)
  return bcdensity

def hall_mob(Rs, scdens):
  '''
  Finds the Hall mobility (cm^2*V^-1*s^-1) of the sample
  '''
  q = 1.602 * (10 **(-19))
  hmob = 1 / (q * scdens * Rs)
  return hmob

def create_file(user_list):
  '''
  Uses the user's input to create appropriate filename for results
  :return: new filename (.csv file)
  '''
  initials = input("\n\"Please enter your initials\": ")
  sample_type = input("\"Please enter the sample type (i.e. ZNO, AZO, etc.)\": ")
  sample_num = input("\"Please enter the sample number\": ")
  new_file = initials + sample_type + sample_num + ".csv"
  user_list.append(initials)
  user_list.append(sample_type)
  user_list.append(sample_num)
  return new_file

def data_write(Rs, p, stype, scdensity, bcdensity, hmob, new_file, current, d, mag_field):
  '''
  :side effect: creates and writes the data to a new csv file
  '''
  write_file = open(new_file, "w")
  write_file.write("Current (nA)")
  write_file.write(",")
  write_file.write("Magnetic Field (G)")
  write_file.write(",")
  write_file.write("Sample Thickness (nm)")
  write_file.write(",")
  write_file.write("Sheet Resistance (ohms/square)")
  write_file.write(",")
  write_file.write("Bulk Resistivity (ohm*meter)")
  write_file.write(",")
  write_file.write("Semiconductor Type")
  write_file.write(",")
  write_file.write("Sheet Carrier Density (cm^-2)")
  write_file.write(",")
  write_file.write("Bulk Carrier Density (cm^-3)")
  write_file.write(",")
  write_file.write("Hall Mobility (cm^2*V^-1*s^-1)")
  write_file.write("\n")
  write_file.write(str(current))
  write_file.write(",")
  write_file.write(str(mag_field))
  write_file.write(",")
  write_file.write(str(d))
  write_file.write(",")
  write_file.write(str(Rs))
  write_file.write(",")
  write_file.write(str(p))
  write_file.write(",")
  write_file.write(str(stype))
  write_file.write(",")
  write_file.write(str(scdensity))
  write_file.write(",")
  write_file.write(str(bcdensity))
  write_file.write(",")
  write_file.write(str(hmob))
  write_file.close()

def running_file(Rs, p, stype, scdens, bcdens, hmob, current, d, mag_field, user_list):
  '''
  Adds the data to a running file
  '''
  old_file = user_list[0] + "Measurements.csv"
  sample = user_list[1] + user_list[2]
  of = open(old_file, "a")
  of.write("\n")
  of.write(sample)
  of.write(",")
  of.write(str(current))
  of.write(",")
  of.write(str(mag_field))
  of.write(",")
  of.write(str(d))
  of.write(",")
  of.write(str(Rs))
  of.write(",")
  of.write(str(p))
  of.write(",")
  of.write(str(stype))
  of.write(",")
  of.write(str(scdens))
  of.write(",")
  of.write(str(bcdens))
  of.write(",")
  of.write(str(hmob))
  of.close()

def Bfield():
  '''
  Use linearization of magetization curve to find the magnitude of the magnetic feild (Tesla--> Gauss) as a function of Current
  :return: magnitude of magnetic field in gauss
  '''
  amps = float(input("Current of magnet (amps)? "))
  dis = float(input("Gap distance between field plates (inches)? "))
  if dis < 0.625:
    tesla = (9.6 / 10) * amps
    gauss = tesla * 10000
    return gauss
  elif 0.625 <= dis < 0.875:
    tesla = (9.2 / 15) * amps
    gauss = tesla * 10000
    return gauss
  elif 0.875 <= dis < 1.25:
    tesla = 0.45 * amps
    print(tesla)
    gauss = tesla * 10000
    print(gauss)
    print(dis, amps, tesla, gauss)
    return gauss
  elif 1.25 <= dis < 1.75:
    tesla = (8.6 / 30) * amps
    gauss = tesla * 10000
    return gauss
  else:
    tesla = (6.8 / 30) * amps
    gauss = tesla * 10000
    return gauss
  
def main():
  '''
  Asks user for necessary information to read and write measurements, records all results to a new file for the current sample and a running file with previous sample listed
  '''
  print("\n------- WELCOME --------")
  #Get user input on data parameters
  filename = input("\n\"Input filename of raw data voltages (V) (.txt)\": ")
  current = float(input("Input Current of Current Source (in nA):  ")) 
  d = float(input("Input sample thickness (in nm): "))
  mag_field = Bfield()
  
  #Initialize lists to populate with raw data
  R1_list = []
  R2_list = []
  R3_list = []
  R4_list = []
  R5_list = []
  R6_list = []
  R7_list = []
  R8_list = []
  H1_list = []
  H2_list = []
  H3_list = []
  H4_list = []
  H5_list = []
  H6_list = []
  H7_list = []
  H8_list = []
  user_list = []

  #Compile the 100 trials for each configuration into a single value for each
  raw_data(filename, R1_list, R2_list, R3_list, R4_list, R5_list, R6_list, R7_list, R8_list, H1_list, H2_list, H3_list, H4_list, H5_list, H6_list, H7_list, H8_list)
  R1 = get_average(R1_list) / (current * 10**-9)
  R2 = get_average(R2_list) / (current * 10**-9)
  R3 = get_average(R3_list) / (current * 10**-9)
  R4 = get_average(R4_list) / (current * 10**-9)
  R5 = get_average(R5_list) / (current * 10**-9)
  R6 = get_average(R6_list) / (current * 10**-9)
  R7 = get_average(R7_list) / (current * 10**-9)
  R8 = get_average(R8_list) / (current * 10**-9)
  H1 = get_average(H1_list)
  H2 = get_average(H2_list)
  H3 = get_average(H3_list)
  H4 = get_average(H4_list)
  H5 = get_average(H5_list)
  H6 = get_average(H6_list)
  H7 = get_average(H7_list)
  H8 = get_average(H8_list)

  #Get the interpreted values
  Rs = sheet_resistance(R1, R2, R3, R4, R5, R6, R7, R8)
  p = find_resistivity(Rs, d)
  V_sum = HV(H1, H2, H3, H4, H5, H6, H7, H8)
  stype = find_type(V_sum)
  scdens = scdensity(current, mag_field, V_sum)
  bcdens = bcdensity(scdens, d)
  hmob = hall_mob(Rs, scdens)

  #Record the data
  new_file = create_file(user_list)
  data_write(Rs, p, stype, scdens, bcdens, hmob, new_file, current, d, mag_field)
  running_file(Rs, p, stype, scdens, bcdens, hmob, current, d, mag_field, user_list)
  error_check(R1, R2, R3, R4, R5, R6, R7, R8)
  print("\n-------- Data saved to new & running file ------------")

main()
