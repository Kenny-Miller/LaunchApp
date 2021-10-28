import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { LauncherService } from 'src/app/services/launcher.service';

@Component({
  selector: 'app-launcher',
  templateUrl: './app-launcher.component.html',
  styleUrls: ['./app-launcher.component.scss']
})
export class AppLauncherComponent implements OnInit {

  loading : boolean = false;

  constructor(private launcherService : LauncherService) { }

  ngOnInit(): void {

  }

  async launchApp(){
    this.loading = true;
    await this.launcherService.launchApp();
    this.loading = false;
  }

}
