import { Component, OnInit } from '@angular/core';
import { SelectBusService } from '../services/selectBus.service';
import { PlacesService } from '../services/places.service'
import { Config } from '../services/places.service'
import { Router } from '@angular/router';
import { NgForm } from '@angular/forms';
import { Journey_Route } from '../models/route.model';
import { AfterViewInit, ElementRef} from '@angular/core';


@Component({
  selector: '.select-bus',
  templateUrl: './select-bus.component.html',
  styleUrls: ['./select-bus.component.css']
})
export class SelectBusComponent implements OnInit {
// ={
//   1109001:'comilla',
//   1109002:'Chittagong',
//   1109003:'Sylet',
//   1109004:'Barisal'
// }

pnumber=1;

place:Place[]=[];
config:Config;
htmlText: string = "";
sources:String[]=["Select Place"];
destinations:String[]=["Select Destination"];
isDisabled1:boolean=false;
isDisabled2:boolean=false;
selectedSource : string = "";
selectedDestination : string = "";
offset:number=0;
allbuses:any;
  constructor(
    private BusService:SelectBusService,
    private placesService:PlacesService,
    private elementRef:ElementRef,
    private router:Router
  ) {
   this.place[0]=new Place()
   }

  ngAfterViewInit() {
    let source = new window['EventSource']('http://localhost:5000/stream');
    source.addEventListener('greeting', this.onClick.bind(this));
  }

  onClick(event){
    this.htmlText = '<div class="col-md-5 slider mt-3">'+event.data+'</div>';
  }

  ngOnInit() {
    

  }

  showConfig() {
  console.log("HELLO");
  this.placesService.getConfig()
    .subscribe((data: Config) => {
        this.config = <Config>data;
        console.log(this.config);
    });

 }



  SearchBus1(form: NgForm) {
    let leaving_form = form.value.leaving_form;
    let destination;
   
  
    this.place.filter(iteam=>{
      if(iteam.key==form.value.going_to){
        destination=iteam.value
      }
    })

    let date = form.value.depart_date;
    let route:Journey_Route = {
      leaving_form: leaving_form,
      going_to: destination,
      date:date
    }
    localStorage.setItem("route", JSON.stringify(route))
    let routeId = form.value.going_to;
    this.BusService.getRoueId(routeId);
    this.router.navigate(['search']);

  }

  SearchBus(form:NgForm){
    localStorage.setItem("source",this.selectedSource);
    localStorage.setItem("destination",this.selectedDestination);
    this.router.navigateByUrl('/search');
  }
  
  leave1(e){
 
    let leavingfrom=e.target.value;
    console.log(leavingfrom)
    if(leavingfrom=='dhaka'){
      this.place= [
        {key:'1109001', value:'Comilla'} ,
        {key:'1109002', value:'Chittagong'} ,
        {key:'1109004', value:'KuaKata'} ,
        {key:'1109005', value:'Coxs Bazar'},
        {key:'1109006', value:'Rajshahi'} 
 
      ]
  }
  else if(leavingfrom=='comilla'){
    this.place= [
      {key:'2209002', value:'Chittagong'} ,
      {key:'2209001', value:'Dhaka'} ,
      {key:'2209003', value:'Rajshahi'} ,
     

    ]
  }
  else if(leavingfrom=='chittagong'){
    this.place= [
      {key:'3309003', value:'Mymensingh'} ,
      {key:'3309001', value:'Dhaka'} ,
      {key:'3309002', value:'Sylet'} ,
   
    ]
  }

}

setSource(e){
  this.selectedSource = e.target.value;
  console.log(this.selectedSource)
}

setDestination(e){
  this.selectedDestination = e.target.value;
  console.log(this.selectedDestination)
}

leave(e){

  console.log("Getting Places you can visit");
  if(this.isDisabled1==false){
  this.placesService.getSources()
    .subscribe((data: Array<Array<String>>) => {
      
        for(var i=0;i<data.length;i++){
          this.sources.push(data[i][0]);
          console.log(data[i][0]);
        }

    });  this.isDisabled1 = true;
    }
}

leave2(e){
  console.log("Getting Destinations you can visit");
  if(this.isDisabled2==false){
  this.placesService.getDestinations(this.selectedSource)
    .subscribe((data: Array<Array<String>>) => {
      
        for(var i=0;i<data.length;i++){
          this.destinations.push(data[i][0]);
          console.log(data[i][0]);
        }

    });  this.isDisabled2 = true;
    }
}


}
export class Place {
  key:string;
  value:string;
}