import { Component, OnInit, OnDestroy, TemplateRef } from '@angular/core';
import { SelectBusService } from '../services/selectBus.service';
import { Subscription } from 'rxjs';
import { Bus } from '../models/bus.model';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router } from '@angular/router';
import { PlacesService } from '../services/places.service';
import { AllBus } from '../models/allbus.model'
@Component({
  selector: 'search-result-info',
  templateUrl: './bus-search-result.component.html',
  styleUrls: ['./bus-search-result.component.css']
})
export class BusSearchResultComponent implements OnInit,OnDestroy {
subscription:Subscription;
buses:Bus[]=[];
modalRef: BsModalRef;
source:string="";
destination:string="";
offset:number = 0;
route=new Object();
allbuses:any=[];
  constructor(
    private BusService:SelectBusService,
    private modalService: BsModalService,
    private placesService : PlacesService,
    private router:Router
  ) { 

  }

  ngOnInit() {
    this.route=JSON.parse(localStorage.getItem("route"));
    
   /**this.subscription= this.BusService.castId.subscribe(
      *res=>this.getAllBus(res)
      *console.log("HERE");
    )**/
    this.getAllBus();


  }

  getChunk(e){
    this.getAllBus();
  }

  getAllBus(){
      console.log("Get All Flights ");
      this.source = localStorage.getItem("source");
      this.destination = localStorage.getItem("destination");
      this.placesService.bookBus(this.source,this.destination,this.offset)
      .subscribe(data=>{
          for (let bus in data){
            this.allbuses.push(data[bus] as AllBus);
          }
          console.log(this.allbuses);
      });
  }
  getAllBus1(res){
    let bus=new Object();
    this.BusService.getBus(res)
    .subscribe(
      res=>{
        for(let key in res){
          bus=res[key];
          bus['$key']=key;
         
 
       this.buses.push(bus as Bus);
   

        }
      }
    )

  }


ngOnDestroy() {
/**
  *this.subscription.unsubscribe();
  */
}

openModal(template: TemplateRef<any>,cost) {
  this.modalRef = this.modalService.show(template);
  // let journey={
  //   route:this.route,
  //   bus_info:bus,
  //   seats:

  // }

  console.log(cost);
  localStorage.setItem("cost",cost);
}
closeModal (){
  this.modalRef.hide();
}

}
