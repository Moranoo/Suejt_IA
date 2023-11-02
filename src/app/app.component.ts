import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  comment: string | undefined;
  warning: boolean = false;

  constructor(private http: HttpClient) {}

  submitComment() {
    this.http.post('http://localhost:5000/analyze', {comment: this.comment}).subscribe((response: any) => {
      if(response.status === 'negative') {
        this.warning = true;
      } else {
        this.warning = false;
      }
    });
  }
}
