import 'package:flutter/material.dart';
import 'package:flutter_stripe/flutter_stripe.dart';


class PaymentPage extends StatelessWidget {
  const PaymentPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Payment Page"),
      ),
      body: Padding(
        padding: EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text('Card Form', style: Theme.of(context).textTheme.headlineMedium),

            const SizedBox(height: 20),
            CardFormField(
              controller: CardFormEditController(),
            )
          ]
        )
        )
    );
  }
}