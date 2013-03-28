def main():
    answer = select_answer(["bwa", "samtools"])
    print "You selected: %s" % answer

def select_answer(valid_answers=[]):
    print "Select one of the following options!"
    print "(type the number to the left of the desired option):"

    valid_answers_enum = dict((i, ans) for i, ans in enumerate(valid_answers))

    answer = ""
    while answer not in valid_answers_enum.iterkeys():
        if not answer in valid_answers_enum.iterkeys() and answer != "":
            print ("Invalid answer! Only the below options (as a number) are allowed!")
        
        for i, valid_ans in valid_answers_enum.iteritems():
            print "[%d] %s" % (i, valid_ans)
        answer = raw_input("Type the number of one of the options above: ")
        try:
            answer = int(answer)
        except:
            print "You have to type a number! Try again ..."
                
    return valid_answers_enum[answer]

if __name__ == '__main__':
    main()        
