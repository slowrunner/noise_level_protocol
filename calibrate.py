#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import time
import subprocess
import os
from subprocess import call
import csv

#change offset here
offset_peak = 45.0
offset_rsm = 40.0
header_csv = ("time", "amplitude", "rms")

#change folder path here
base_folder = "/home/pi/Carl/Projects/noise_level_protocol/"

#change duration to detect here
dur = " 10 "  # or 120

try:
    while True:
        #pkill because sometimes my microphone was busy
        subprocess.call("pkill -9 sox | pkill -9 arecord",shell= True)
        time.sleep( 1 )
        
        #time
        filedate = time.strftime("%Y%m%d-%H%M%S")
        filename = base_folder + "mp3/" + time.strftime("%Y%m%d") + "/" + filedate + ".mp3"
        filename_csv = base_folder + "csv/" + time.strftime("%Y%m%d") + ".csv"
        filedate_csv  = time.strftime("%Y-%m-%d %H:%M")
        terminal_time = time.strftime("%H:%M ")
        
        #record for duration
        print("Listening for " + dur + "seconds...")
        # arecord options:
        #   original -f dat =  (16 bit little endian, 48000, stereo) [-f S16_LE -c2 -r48000]
        #   --quiet  suppress messages
        #   --buffer-size=192ms (interrupts at 4x buffersize giving 4 times sampling for 48kHz
        #   -t raw   output file type: raw = PCM data no header
        #   --fatal-errors  disables recovery attempts on errors

        # lame (encodes to variable bit rate mp3) options:
        #   -r input is raw (headerless) PCM
        #   --quiet   no messages to std out
        #   --preset standard is same as -V 2  VBR Quality  about 200kbps
        #   -  read from stdin
        #  (output mp3 encoded data to filename)
#        subprocess.call("arecord -D hw:1,0 -d " + dur + " -v --fatal-errors --buffer-size=192000 -f dat -t raw --quiet | lame -r --quiet --preset standard - " + filename,shell= True)
#        subprocess.call("arecord -D hw:1,0 -d " + dur + "  --fatal-errors --buffer-size=192000 -f S16_LE -r48000 -c1 -t raw --quiet | lame -r  --quiet --preset standard - " + filename + " 2>&1",shell= True)
        subprocess.call("arecord -D hw:1,0 -d " + dur + "  --fatal-errors --buffer-size=192000 -f S16_LE -r48000 -c1 --quiet | lame  --quiet --preset standard - " + filename + " 2>&1",shell= True)

        # SoX sound exchange (swiss knife for audio)
        # sox options:
        #   -n  null output file - throw away output
        #   stat 
        proc = subprocess.getoutput("sox " + filename + " -n stat 2>&1 | grep 'Maximum amplitude' | cut -d ':' -f 2")
#        proc = subprocess.getoutput("sox " + filename + " -n stat 2>&1 " )
        proc_rms = subprocess.getoutput("sox " + filename + " -n stat 2>&1 | grep 'RMS.*amplitude' | cut -d ':' -f 2")
#        os.system('clear')
        proc1 = proc.strip()
        proc1 = float(proc1)
        proc_rms = proc_rms.strip()
        proc_rms = float(proc_rms)
        
        #test your microphone in 5 dB steps and create the function e.g. with mycurvefit.com
        #Fkt 3 30-80 dB
#        proc3 = 83.83064 + (28.34183 - 83.83064)/(1 + (proc1/0.04589368)**1.006258)
        proc3 = 80 + (30 - 80)/(1 + (proc1/0.04)**1.0)
        #Fkt RMS 30-80 dB
        proc3_rms = 87.69054 + (23.81973 - 87.69054)/(1 + (proc_rms/0.01197014)**0.7397556)
        
        #add db filextentions: peak - rms
        ext_peak = int(round(proc3, 0))
        ext_rms = int(round(proc3_rms, 0))
        
        
        print("Measured values - peak:" + str(proc1) + " rms: " + str(proc_rms) + "\n")
        
        #csv
        file_exists = os.path.isfile(filename_csv)
        daten_csv = (filedate_csv, proc3, proc3_rms)
        with open(filename_csv, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header_csv)
            writer.writerow(daten_csv)
        
#        if proc3 >= offset_peak or proc3_rms >= offset_rsm:
#                    print(terminal_time + "Sound detected - save: " + filedate + ".mp3 \n")
#                    os.rename(filename, base_folder + "mp3/" + time.strftime("%Y%m%d") + "/" + filedate + "-" + str(ext_peak) + "-" + str(ext_rms) + ".mp3")
#                    time.sleep( 3 )
                    #os.system('clear')
                    
#        else: 
#            print(terminal_time + "No sound detected, delete: " + filedate + ".mp3 \n")
            os.remove(filename)
            time.sleep( 3 )
            #os.system('clear')
            
except KeyboardInterrupt:
        subprocess.call("pkill -9 sox | pkill -9 arecord",shell= True)
        print('End')
