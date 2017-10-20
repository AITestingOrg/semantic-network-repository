import { Component } from '@angular/core';
import {DataSource} from '@angular/cdk';
import {BehaviorSubject} from 'rxjs/BehaviorSubject';
import {Observable} from 'rxjs/Observable';
import {FormControl} from '@angular/forms';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/observable/merge';
import 'rxjs/add/operator/map';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'app';
  displayedColumns = ['userId', 'userName', 'progress', 'color'];
  exampleDatabase = new ExampleDatabase();
  dataSource: ExampleDataSource | null;
  opts: string[]
  myControl = new FormControl();
  filteredOptions: Observable<string[]>;

  ngOnInit() {
    this.dataSource = new ExampleDataSource(this.exampleDatabase);
    this.opts = OPS
    this.filteredOptions = this.myControl.valueChanges
      .startWith(null)
      .map(val => val ? this.filter(val) : this.opts.slice());
  }

  filter(val: string): string[] {
    return this.opts.filter(opt => new RegExp(`^${val}`, 'gi').test(opt))
  }
}


/** Constants used to fill up our data base. */
const VALUES = ['0', '1', 'STE', 'SE'];
const DECISIONS = ['Maia', 'Asher', 'Olivia', 'Atticus', 'Amelia', 'Jack',
'Charlotte', 'Theodore', 'Isla', 'Oliver', 'Isabella', 'Jasper',
'Cora', 'Levi', 'Violet', 'Arthur', 'Mia', 'Thomas', 'Elizabeth'];
const OPS = ['is a', 'has a', 'equals', 'belongs to', 'of type', 'never equals']

export interface Rule {
  id: string;
  value: string;
  operator: string;
  decision: string;
}

/** An example database that the data source uses to retrieve data for the table. */
export class ExampleDatabase {
/** Stream that emits whenever the data has been modified. */
dataChange: BehaviorSubject<Rule[]> = new BehaviorSubject<Rule[]>([]);
get data(): Rule[] { return this.dataChange.value; }

constructor() {
  // Fill up the database with 100 users.
  for (let i = 0; i < 100; i++) { this.addRule(); }
}

/** Adds a new user to the database. */
addRule() {
  const copiedData = this.data.slice();
  copiedData.push(this.createRule());
  this.dataChange.next(copiedData);
}

/** Builds and returns a new User. */
private createRule() {
  const value =
      DECISIONS[Math.round(Math.random() * (DECISIONS.length - 1))] + ' ' +
      DECISIONS[Math.round(Math.random() * (DECISIONS.length - 1))].charAt(0) + '.';

  return {
    id: (this.data.length + 1).toString(),
    operator: OPS[Math.round(Math.random() * (OPS.length - 1))],
    value: value,
    decision: VALUES[Math.round(Math.random() * (VALUES.length - 1))]
  };
}
}

/**
* Data source to provide what data should be rendered in the table. Note that the data source
* can retrieve its data in any way. In this case, the data source is provided a reference
* to a common data base, ExampleDatabase. It is not the data source's responsibility to manage
* the underlying data. Instead, it only needs to take the data and send the table exactly what
* should be rendered.
*/
export class ExampleDataSource extends DataSource<any> {
constructor(private _exampleDatabase: ExampleDatabase) {
  super();
}

/** Connect function called by the table to retrieve one stream containing the data to render. */
connect(): Observable<Rule[]> {
  return this._exampleDatabase.dataChange;
}

disconnect() {}
}