import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  private questionMode = false
  constructor() { }

  ngOnInit() {
  }

  private toggleSearch(event) {
    this.questionMode = false
  }

  private toggleQuestion(event) {
    this.questionMode = true
  }

}
