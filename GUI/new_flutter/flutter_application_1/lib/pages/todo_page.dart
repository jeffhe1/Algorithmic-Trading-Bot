import 'package:flutter/material.dart';

class ToDoPage extends StatefulWidget {
  const ToDoPage({super.key});

  @override
  State<ToDoPage> createState() => _ToDoPageState();
}

class _ToDoPageState extends State<ToDoPage> {

  // Text editing controller
  TextEditingController myController = TextEditingController();

  // greeting message variable
  String greetingMessage="";

  // Method
  void greetUser(){
    setState(() { 
      String userName = myController.text;
      greetingMessage = "I Love " + userName;
    });
  }

  // Direct to pages
  void direct_to(name) {
    Navigator.pop(context);
    Navigator.pushNamed(context, name);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.pink[200],
      appBar: AppBar(
        leading: Icon(Icons.favorite),
        centerTitle: true, 
        title: Icon(Icons.favorite), 
        backgroundColor: Colors.pinkAccent, 
        actions: [Icon(Icons.favorite)],
        elevation: 0,  
      ),
      body: Center(child: 
        // Text Field
        Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            //Icon
            Icon(Icons.favorite, size: 100, color:Colors.red[800]),
            // Greeting Message
            Text(greetingMessage, style: TextStyle(color: Colors.red[800], fontSize: 64)),
            // Text Field
            TextField(
              controller: myController,
              textAlign: TextAlign.center,
              decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                  borderSide: BorderSide(color: Colors.amber,width:3),
                ),
                hintText: "Type your name",

                ),
              ),

            // Button
            ElevatedButton(onPressed: greetUser, child: Text("Tap")),

            // Payment Button
            ElevatedButton(onPressed: (){
              Navigator.pop(context);
              Navigator.pushNamed(context, '/paymentpage');
            }, child: Text("Go to Payment"))
          ]
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: [
          BottomNavigationBarItem(icon: Icon(Icons.favorite), label: "Abby"),
          BottomNavigationBarItem(icon: Icon(Icons.favorite), label: "Abby"),
          BottomNavigationBarItem(icon: Icon(Icons.favorite), label: "Abby"),
          ],
        backgroundColor: Colors.pinkAccent,
        ),
      drawer: Drawer(
        backgroundColor: Colors.pink[100],
        child: Column(
          children: [
            DrawerHeader(child: Text("Abby")),

            // List Tile
            ListTile(
              autofocus: true,
              leading: Icon(Icons.payment),
              title: Text("Payment"),
              onTap: () {
                Navigator.pop(context);
                Navigator.pushNamed(context, '/paymentpage');
              }
            )
          ],
          )
      )
    );
  }
}