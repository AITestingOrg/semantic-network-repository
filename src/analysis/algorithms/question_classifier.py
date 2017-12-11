def is_question(parsed_frag):
    likelihood = 0
    begins_with_verb = False
    beings_with_wh_word = False

    # the fragment starts with a verb
    # now we need to check if this is a WH or auxilary verb
    print(parsed_frag[0].pos_)
    if parsed_frag[0].pos_ == 'VERB':
        begins_with_verb = True

        # does this fragment start with 'to be', if so it is most likely a quesiton.
        if parsed_frag[0].lemma_ == 'be':
            return True

    print(parsed_frag[0].tag_)
    if parsed_frag[0].tag_ == 'WH':
        beings_with_wh_word = True
        likelihood = 0.75

        # check if this is an aux verb

    # subject verb inversion