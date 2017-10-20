import { BrowserModule } from '@angular/platform-browser';
import { NgModule,  } from '@angular/core';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {
  MdButtonModule,
  MdCheckboxModule,
  MdInputModule,
  MdTableModule,
  MdSelectModule,
  MdAutocompleteModule
} from '@angular/material';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {CdkTableModule} from '@angular/cdk';
import 'hammerjs';

import { AppComponent } from './app.component';
import { HeaderComponent } from './layout/header/header.component';
import { SearchComponent } from './layout/header/search/search.component';
import { NavigationComponent } from './layout/header/navigation/navigation.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    SearchComponent,
    NavigationComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MdButtonModule,
    MdCheckboxModule,
    MdInputModule,
    MdTableModule,
    CdkTableModule,
    MdSelectModule,
    FormsModule,
    ReactiveFormsModule,
    MdAutocompleteModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }