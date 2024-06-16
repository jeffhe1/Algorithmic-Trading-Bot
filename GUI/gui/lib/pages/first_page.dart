// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import "package:flutter/material.dart";
import "package:gui/pages/home_page.dart";
import "package:gui/pages/profile_page.dart";
import "package:gui/pages/setting_page.dart";

class FirstPage extends StatefulWidget {
  FirstPage({super.key});

  @override
  State<FirstPage> createState() => _FirstPageState();
}

class _FirstPageState extends State<FirstPage> {
  // keeps track of the current page to display
  int _selectedIndex = 0;

  // this method upadates the new selected index
  void _navigateBottomBar(int index) {
   setState(() {
     _selectedIndex = index;
   });
  }

  // mappings
  final List _pages = [
    // homepage
    HomePage(),

    // profile page
    ProfilePage(),

    // settings page
    SettingPage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("First Page")),
      body: _pages[_selectedIndex],
      drawer: Drawer(
        backgroundColor: Colors.amber[200],
        child: Column(
          children: [
            // Drawer Header
            DrawerHeader(child: Icon(Icons.favorite,size:48),),

            // Home List tile
            ListTile(autofocus: true,leading: Icon(Icons.home), title: Text("Home"),
            onTap: (){
              //pop the drawer
              Navigator.pop(context);

              // Go Home Page
              Navigator.pushNamed(context, '/homepage');
            },
            ),

            // Settings page list tile
            ListTile(leading: Icon(Icons.settings), title: Text("Settings"),
            onTap: () {
              //pop the drawer
              Navigator.pop(context);

              // Go Setting Page
              Navigator.pushNamed(context, '/settingpage');
            },
            )
          ],
        )
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: _navigateBottomBar,
        items: [
          // home
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home',),
          // profile
          BottomNavigationBarItem(icon: Icon(Icons.person),label: "Profile"),
          // setting
          BottomNavigationBarItem(icon: Icon(Icons.settings),label: "Settings"),
        ]
      ),
    );
  }
}