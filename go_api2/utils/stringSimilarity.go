package utils

import (
	"math"
	"strings"
)

//nb_of_selection is the number of times the food has been clicked on the client
// its a strong indicator of the popularity
func CalculateSimilarityStringScores(string *string, searchText string) *uint64 {
	//var similarity_score int

	stringTest := *string
	stringTest = strings.ToLower(stringTest)
	searchTestLower := strings.ToLower(searchText)
	var similarity_score uint64 = 0
	consecutiv_chars := 0
	str_len := len(stringTest)
	last_same_index_search_text := -1
	for i := 0; i < str_len; i++ {
		char_a := rune(stringTest[i])
		last_same_index_search_text = getLastSameIndexSearchText(consecutiv_chars, last_same_index_search_text, char_a, searchText, i, str_len, stringTest)

		if last_same_index_search_text != -1 {
			consecutiv_chars++
		}

		if i == str_len-1 || (last_same_index_search_text == -1 && consecutiv_chars > 0) {
			new_score := uint64(math.Pow(float64(consecutiv_chars), 4))
			index_char_before_consecutiv := i - consecutiv_chars
			if index_char_before_consecutiv == 0 {
				first_word_letter := stringTest[i-consecutiv_chars]

				if first_word_letter == searchTestLower[0]{
					new_score *= uint64(math.Pow(float64(consecutiv_chars), 3))
				}
			}
			similarity_score += new_score
			consecutiv_chars = 0
		}
	}
	final_score := (similarity_score * 100/ uint64(str_len))
	return &final_score
}


func getLastSameIndexSearchText(consecutiv_chars int, last_same_index_search_text int, char_a rune, searchText string, i int, str_len int, stringTest string) int {
	if consecutiv_chars == 0 {
		last_same_index_search_text = GetSameCharIndex(&char_a, searchText)
	} else if i < str_len-1 && (len(searchText)-1 > last_same_index_search_text) {
		same := stringTest[i] == searchText[last_same_index_search_text+1]
		if same {
			last_same_index_search_text++
		} else {
			last_same_index_search_text = -1
		}
	} else {
		last_same_index_search_text = -1
	}
	return last_same_index_search_text
}

func GetSameCharIndex(targetChar *rune, searchText string) int {
	for j := 0; j < len(searchText); j++ {
		var char_b rune
		char_b = rune(searchText[j])
		if *targetChar == char_b {
			return j
		}
	}
	return -1
}