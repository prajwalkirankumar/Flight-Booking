import { Component, OnInit } from '@angular/core';
import { PlacesService } from '../services/places.service';
import { Chat } from '../models/chat.model';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {

  constructor(private placesService : PlacesService) {
        
   }

  ngOnInit() {
  }
  sendertext:String="";
//  divText:String='<div class="container"><img src="/assets/bandmember.png" alt="Avatar" //style="width:100%;"><p>Hello. How are you today?</p><span class="time-right">11:00</span></div>';

  obj = {text:'Hello',time:'time-left',class:'right'};
  chats:Chat[] = [this.obj];


  send(){
  	console.log(this.sendertext);
    if(this.sendertext!=""){
  	   this.chats.push({text:this.sendertext as string,time:'time-right',class:''});

       this.placesService.sendChat(this.sendertext)
      .subscribe(data=>{
          console.log(data);
          this.chats.push({text:data as string,time:'time-left',class:'right'});
      });
    }

  }

}
