import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subscription } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LauncherService {

  private _apps : BehaviorSubject<string[]> = new BehaviorSubject<string[]>([]);
  public apps$ : Observable<string[]> = this._apps.asObservable();

  private _selectedApp : BehaviorSubject<string> = new BehaviorSubject<string>('');

  constructor(private http: HttpClient) {
    this.getApps();
  }

  async getApps(){
    this.http.get<string[]>(`${environment.launcherUrl}/getApps`).subscribe(
      (response) =>{
        this._apps.next(response);
      },
      (error) =>{
        console.error("Can't get App list");
      }
    )
  }

  changeSelectedApp(appName : string){
    if(appName){
      this._selectedApp.next(appName);
    }
  }

  async launchApp() {
    const app = this._selectedApp.getValue();
    
    await this.http.post(`${environment.launcherUrl}/launchApp`, {app:app}).toPromise().then(
      (res) => {

      },
      (error) =>{
        console.log('error');
      }
    )
  }
}
