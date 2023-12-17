import json
import time
import csv

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
            print(f"The Passport Number field on record {i+1} is not correct.")
        if calcCd2 != cd2:
            print(f"The Birth Date field on record {i+1} is not correct.")
        if calcCd3 != cd3:
            print(f"The Expiration Date field on record {i+1} is not correct.")
        if calcCd4 != cd4:
            print(f"The Personal Number field on record {i+1} is not correct.")

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
    def decode_mrz(num_lines):
        n = num_lines
        mrz_system = MRTDSystem()
        decoded_records = []

        with open("records_encoded.json", 'r') as file:
            data = json.load(file)
        records_encoded = data.get("records_encoded", [])
        for i, record in enumerate(records_encoded[:n]):
            line1, line2 = mrz_system.scan_mrz(record)
            decoded_info = mrz_system.decode_mrz_line(line1, line2, i)
            decoded_records.append(decoded_info)

        return decoded_records
    
    @staticmethod
    def encode_mrz_line(line1_data, line2_data):
        cd1 = MRTDSystem.check_digit(line2_data["passport_number"])
        cd2 = MRTDSystem.check_digit(line2_data["birth_date"])
        cd3 = MRTDSystem.check_digit(line2_data["expiration_date"])
        cd4 = MRTDSystem.check_digit(line2_data["personal_number"])

        full_name = line1_data["given_name"]
        names = full_name.split(" ")
        if len(names) >= 2:
            first_name = names[0]
            middle_name = " ".join(names[1:])
        else:
            first_name = full_name
            middle_name = ""

        if len(names) >= 2:
            first_name = names[0]
            middle_name = " ".join(names[1:])

        line1_empty_chars = 44 - len(f"P<{line1_data['issuing_country']}{line1_data['last_name']}<<{line1_data['given_name']}")
        encoded1 = f"P<{line1_data['issuing_country']}{line1_data['last_name']}<<{first_name}<{middle_name}{'<' * line1_empty_chars}"
        encoded2 = f"{line2_data['passport_number']}{cd1}{line2_data['country_code']}{line2_data['birth_date']}{cd2}{line2_data['sex']}{line2_data['expiration_date']}{cd3}{line2_data['personal_number']}<<<<<<{cd4}"

        return encoded1, encoded2

        

    @staticmethod
    def encode_mrz(num_lines):
        n = num_lines
        mrz_system = MRTDSystem()
        encoded_records = []
        with open("records_decoded.json", 'r') as file:
            data = json.load(file)
        records_decoded = data.get("records_decoded", [])
        for i, record in enumerate(records_decoded[:n]):
            line1_data = {
            "issuing_country": record["line1"]["issuing_country"],
            "last_name": record["line1"]["last_name"],
            "given_name": record["line1"]["given_name"],
            }

            line2_data = {
            "passport_number": record["line2"]["passport_number"],
            "country_code": record["line2"]["country_code"],
            "birth_date": record["line2"]["birth_date"],
            "sex": record["line2"]["sex"],
            "expiration_date": record["line2"]["expiration_date"],
            "personal_number": record["line2"]["personal_number"],
            }
            encoded1, encoded2 = mrz_system.encode_mrz_line(line1_data, line2_data)
            encoded_info = {f"record{i+1}_line1": encoded1,
                            f"record{i+1}_line2": encoded2}
            encoded_records.append(encoded_info)

        return encoded_records

    @staticmethod
    def runtimes():
        lines = [100,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
        with open("decode_runtimes.csv", mode="w", newline="") as csvfile:
            fieldnames = ["Lines Decoded", "Runtime"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for number in lines:
                start_time = time.time()
                MRTDSystem.decode_mrz(number)
                runtime = time.time() - start_time

                # Write the results to the CSV file
                writer.writerow({
                    "Lines Decoded": number,
                    "Runtime": runtime
                })

        with open("encode_runtimes.csv", mode="w", newline="") as csvfile:
            fieldnames = ["Lines Encoded", "Runtime"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for number in lines:
                start_time = time.time()
                MRTDSystem.encode_mrz(number)
                runtime = time.time() - start_time

                # Write the results to the CSV file
                writer.writerow({
                    "Lines Encoded": number,
                    "Runtime": runtime
                })



if __name__ == "__main__":

    MRTDSystem.runtimes()