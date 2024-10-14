class TestShortPhrase:
    def test_short_phrase(self):
        # Defining the expected phrase length
        expected_phrase_length = 15
        actual_phrase_length = 0
        # We are checking that user set a phrase
        while actual_phrase_length == 0:
            phrase = input("Set a phrase here to proceed: ")
            # Getting the set phrase's length
            actual_phrase_length = len(phrase)

        # Testing the length of set phrase
        assert actual_phrase_length <= expected_phrase_length, f"The expected phrase length is less than " \
                                                               f"{expected_phrase_length}" \
                                                               f" but got {actual_phrase_length}"
