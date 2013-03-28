import re

def main():
    sbatch_config = SbatchConfig()
    sbatch_config.show_config_wizard()
    sbatch_config.print_formatted()
    #sbatch_config.save_to_file()

class HpcConfig(object):
    def __construct(self):
        pass
    
    def select_answer(self, message_text, valid_answers=[]):
        print "-"*80
        print "%s: " % message_text
    
        valid_answers_enum = dict((i+1, ans) for i, ans in enumerate(valid_answers))
        answer = ""
        while answer not in valid_answers_enum.iterkeys():
            if answer != "":
                print "Invalid answer! Only the below options (as a number) are allowed!"
            
            for i, valid_ans in valid_answers_enum.iteritems():
                print "[%d] %s" % (i, valid_ans)
            answer = raw_input("Type the number of one of the options above: ")
            try:
                answer = int(answer)
            except:
                print "You have to type a number! Try again ..."
                    
        return valid_answers_enum[answer]
        
        
    def validate_input(self, message_text, validation_pattern):
        answer = ""
        print "-"*80
        while not bool(re.match(validation_pattern, answer)):
            if answer != "":
                print "Invalid answer! Try again ..."
            answer = raw_input("%s: " % message_text)
        return answer

    def get_boolean_answer(self, message_text):
        valid_answers = ["n", "y", "N", "Y", "no", "yes", "No", "Yes"]
        answer = ""
        print "-"*80
        while answer not in valid_answers:
            if answer != "":
                print "Invalid answer! Try again ..."
            answer = raw_input("%s [Y/n]" % message_text)
        if answer in ["n", "N", "no", "No"]:
            return False
        elif answer in ["y", "Y", "yes", "Yes"]:
            return True

class SbatchConfig(HpcConfig):
    def __construct(self):
        self.project = ""
        self.partition = ""
        self.time = ""
        self.job_name = ""
        self.cores_cnt = 0
        self.nodes_cnt = 0
        self.qos_short = False
        
    def show_config_wizard(self):
        self.project = self.select_answer("Select project", ["staff", "b2011221"])
        self.partition = self.select_answer("Select partition", ["core", "node"])
        self.time = self.validate_input("Specify job running time ([d-]hh:mm:ss)", "([0-9]\-)?[0-9]{2}:[0-9]{2}:[0-9]{2}")
        self.job_name = self.validate_input("Give a job name", "[a-zA-Z0-9\_\-\.]")
        self.cores_cnt = self.select_answer("Select number of cores", range(1,8+1))
        if self.partition == "node":        
            self.nodes_cnt = self.validate_input("Select number of nodes (1-348)", "\d{1,3}")
        self.qos_short = self.get_boolean_answer("Add --qos=short flag?")
        
    def get_formatted(self):
        output = "\n#!/bin/bash -l\n"
        output += "#SBATCH -A %s\n" % self.project
        output += "#SBATCH -p %s\n" % self.partition
        output += "#SBATCH -t %s\n" % self.time
        output += "#SBATCH -J %s\n" % self.job_name
        output += "#SBATCH -n %s\n" % self.cores_cnt
        if self.partition == "node":
            output += "#SBATCH -N %s\n" % self.nodes_cnt
        if self.qos_short:
            output += "#SBATCH --qos=short\n"
        return output
        
    def print_formatted(self):
        sbatch_code = self.get_formatted()
        print "-"*80
        print "Below follows the resulting SBATCH script:"
        print "-"*80
        print sbatch_code        


if __name__ == '__main__':
    main()        
