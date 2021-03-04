package utils

func ThrowError(error error) {
	if error != nil {
		println(error)
	}
}
