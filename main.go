package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

type TodayPrice struct {
	SN          int    `json:"S.N."`
	TradedComp  string `json:"Traded Company"`
	NoOfTrans   string `json:"No. of trans"`
	MaxPrice    string `json:"MaxPrice"`
	MinPrice    string `json:"MinPrice"`
	ClosePrice  string `json:"ClosePrice"`
	TradeShares string `json:"TradeShares"`
	Amount      string `json:"Amount"`
	PrevClose   string `json:"PrevClose"`
	Diff        string `json:"Diff"`
}

func index(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "<a href=\"/todaysprice\">Todays price</a>")
}

func todaysprice(w http.ResponseWriter, req *http.Request) {
	// jsonFile, err := os.Open("./json/todaysprice.json")
	jsonFile, err := ioutil.ReadFile("./json/todaysprice.json")
	if err != nil {
		log.Fatal(err)
	}

	var todaysprice []TodayPrice
	err2 := json.Unmarshal(jsonFile, &todaysprice)

	if err2 != nil {
		log.Fatal(err2)
	}
	w.Header().Set("Content-type", "application/json")
	json.NewEncoder(w).Encode(todaysprice)
}

func main() {
	http.HandleFunc(`/`, index)
	http.HandleFunc(`/todaysprice`, todaysprice)

	port := `:6767`
	fmt.Printf("Starting server at %v\n", port)

	http.ListenAndServe(port, nil)
}
