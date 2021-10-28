import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { LauncherService } from 'src/app/services/launcher.service';

@Component({
  selector: 'app-selector',
  templateUrl: './app-selector.component.html',
  styleUrls: ['./app-selector.component.scss']
})
export class AppSelectorComponent {

  apps$ : Observable<string[]>

  constructor(private launcherService : LauncherService) { 
    this.apps$ = this.launcherService.apps$;
  }

  onSelection(val : any){
    this.launcherService.changeSelectedApp(val.option.value);
  }

}
