import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class PlacesService {

    constructor(private http: HttpClient) { }

    configUrl = 'assets/config.json';
    sourcesUrl = 'http://localhost:5000/getSources';
    destinationsUrl = 'http://localhost:5000/getDestinations';
    bookBusUrl = 'http://localhost:5000/getAllFlights';
    sendChatUrl = 'http://localhost:5000/chat'
    places : any;

	getConfig() {
	  return this.http.get<Config>(this.configUrl);
	}

	getSources() {
		return this.http.get(this.sourcesUrl);
	}

	getDestinations(source) {
		return this.http.get(this.destinationsUrl+'/'+source);
	}

	bookBus(source,destination,offset){

		return this.http.get(this.bookBusUrl+'/'+source+'/'+destination+'/'+offset);
	}

	getFlights(){
		return this.places;
	}

	sendChat(msg){
	//return "HELLO";
		return this.http.get<string>(this.sendChatUrl+'/'+msg);
	}
}

export interface Config {
  heroesUrl: string;
  textfile: string;
}

export interface Sources {
	sources: Array<Array<String>>;
}

