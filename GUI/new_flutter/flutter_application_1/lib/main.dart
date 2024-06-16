import 'package:flutter/material.dart';
import 'package:flutter_application_1/pages/payemnt_page.dart';
import 'package:flutter_application_1/pages/todo_page.dart';

import 'package:flutter_application_1/screens/.env';
import 'package:flutter_stripe/flutter_stripe.dart';


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  Stripe.publishableKey = stripePublishableKey;
  await Stripe.instance.applySettings();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {

  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: ToDoPage(),
      routes: {
        '/paymentpage' : (context) => PaymentPage(),
      },
    );
  }
}
