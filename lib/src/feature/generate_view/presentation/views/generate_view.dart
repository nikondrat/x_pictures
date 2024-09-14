import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class GenerateView extends StatelessWidget {
  const GenerateView({super.key});

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return MultiProvider(
        providers: [
          Provider<GenerateViewStore>(
            create: (_) => GenerateViewStore(),
            dispose: (context, value) => value.dispose(),
          ),
          Provider<GenerateStore>(
              create: (c) => GenerateStore(
                    restClient: c.read<Dependencies>().restClient,
                    viewStore: c.read<GenerateViewStore>(),
                  ))
        ],
        builder: (context, child) {
          final store = context.read<GenerateStore>();

          return Scaffold(
            appBar: AppBar(
              title: Text(
                t.generateView.title,
                style: textTheme.bodyMedium!.copyWith(
                  fontSize: 17,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
            body: AppBody(
              builder: (windowWidth, windowHeight, windowSize) => GenerateBody(
                  store: store,
                  windowWidth: windowWidth,
                  windowHeight: windowHeight),
            ),
          );
        });
  }
}
