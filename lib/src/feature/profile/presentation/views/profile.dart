import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class ProfileView extends StatelessWidget {
  const ProfileView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: AppBody(
        builder: (windowWidth, windowHeight, windowSize) {
          return SafeArea(
            child: Padding(
                padding: HorizontalSpacing.centered(windowWidth),
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      // TODO change
                      FilledButton(
                          onPressed: () =>
                              router.goNamed(AppViews.settingsView),
                          child: Text('go to settings')),
                    ],
                  ),
                )),
          );
        },
      ),
    );
  }
}
