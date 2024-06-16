// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:gui/pages/first_page.dart';
import 'package:gui/pages/home_page.dart';
import 'package:gui/pages/profile_page.dart';
import 'package:gui/pages/setting_page.dart';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // functions & methods

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: FirstPage(),
      routes: {
        '/firstpage': (context) => FirstPage(),
        '/homepage': (context) => HomePage(),
        '/settingpage': (context) => SettingPage(),
        '/profilepage': (context) => ProfilePage(),
      }
    );
  }
}
