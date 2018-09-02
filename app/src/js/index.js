import 'bootstrap';
import 'pagerjs';
import ko from 'knockout';
import App from './App';
import '../sass/main.scss';

/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
const app = {
  // Application Constructor
  initialize () {
    document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
  },

  // deviceready Event Handler
  //
  // Bind any cordova events here. Common events are:
  // 'pause', 'resume', etc.
  onDeviceReady () {
    this.receivedEvent('deviceready');
  },

  // Update DOM on a Received Event
  receivedEvent () {
    const appViewModel = new App();

    pager.extendWithPage(appViewModel);
    pager.start();

    ko.applyBindings(appViewModel);
    appViewModel.initialize();

    /*
    const m = moment().add(1, 'minute');

    cordova.plugins.notification.local.schedule({
      id: 1,
      title: 'My first notification',
      text: 'Thats pretty easy...',
      foreground: true,
      trigger: {
        every: {
          hour: m.get('hours'),
          minute: m.get('minutes'),
        },
      },
    });
    */
  },
};

app.initialize();
