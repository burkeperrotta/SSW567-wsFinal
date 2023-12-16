import json
import time

class MRTDSystem:
    @staticmethod
    def scan_mrz(line):
        # Modified function to split each line at the semicolon and return two strings
        line1, line2 = line.strip().split(';')
        return line1, line2

    @staticmethod
    def decode_mrz_line(line1, line2, i):
        mrz_system = MRTDSystem()
        # Modified function to use scan_mrz and populate the dictionary as specified
        decoded_info = {"Doc Type": line1[0], "Issuing Country": line1[2:5],
                        "Last": line1[5:line1.find("<<")].replace("<", " "),
                        "First": line1[line1.find("<<")+2:line1.find("<", line1.find("<<")+2)].replace("<", " "),
                        "Middle": line1[line1.find("<", line1.find("<<")+2)+1:].replace("<", ""), 
                        "Passport Number": line2[:9], "Country Code":line2[10:13], 
                        "Birth Date":line2[13:19], "Sex": line2[20], "Expiration Date":line2[21:27],
                        "Personal Number": line2[28:37]}
        
        cd1 = line2[9]
        cd2 = line2[19]
        cd3 = line2[27]
        cd4 = line2[43]
        cdInfo1 = decoded_info["Passport Number"]
        cdInfo2 = decoded_info["Birth Date"]
        cdInfo3 = decoded_info["Expiration Date"]
        cdInfo4 = decoded_info["Personal Number"]
        calcCd1 = mrz_system.check_digit(cdInfo1)
        calcCd2 = mrz_system.check_digit(cdInfo2)
        calcCd3 = mrz_system.check_digit(cdInfo3)
        calcCd4 = mrz_system.check_digit(cdInfo4)

        if calcCd1 != cd1:
            print(f"The Passport Number field on record {i} is not correct.")
        if calcCd2 != cd2:
            print(f"The Birth Date field on record {i} is not correct.")
        if calcCd3 != cd3:
            print(f"The Expiration Date field on record {i} is not correct.")
        if calcCd4 != cd4:
            print(f"The Personal Number field on record {i} is not correct.")

        return decoded_info
    
    @staticmethod
    def check_digit(cd_info):
    
        weights = [7, 3, 1, 7, 3, 1, 7, 3, 1]
        total = sum(
            (ord(char) - ord("A") + 10 if char.isalpha() else int(char) if char.isnumeric() else 0)
            * weight
            for char, weight in zip(cd_info, weights)
    )

        return str(total % 10)

    
    @staticmethod
    def decode_mrz():
        n=5 # change this number for number of records to run and time
        start_time = time.time()
        mrz_system = MRTDSystem()
        decoded_records = []

        with open("records_encoded.json", 'r') as file:
            data = json.load(file)
        records_encoded = data.get("records_encoded", [])
        for i, record in enumerate(records_encoded[:n]):
            line1, line2 = mrz_system.scan_mrz(record)
            decoded_info = mrz_system.decode_mrz_line(line1, line2, i)
            decoded_records.append(decoded_info)

        end_time = time.time()
        run_time = end_time - start_time
        print(f"Decoding {n} lines took {run_time:.4f} seconds")
        return decoded_records
    

if __name__ == "__main__":
    # Call the decode_mrz function with the desired number of lines
    decoded_records = MRTDSystem.decode_mrz()