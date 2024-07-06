import 'dart:async';

import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class StudyingView extends StatefulWidget {
  final String url;
  final Widget child;
  const StudyingView({super.key, required this.url, required this.child});

  @override
  State<StudyingView> createState() => _StudyingViewState();
}

class _StudyingViewState extends State<StudyingView> {
  bool showView = false;

  @override
  void initState() {
    Timer(const Duration(seconds: 5), () {
      setState(() {
        showView = true;
      });
    });
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return showView
        ? widget.child
        : Scaffold(
            body: AppBody(
              builder: (windowWidth, windowHeight, windowSize) {
                return Padding(
                  padding: HorizontalSpacing.centered(windowWidth) +
                      const EdgeInsets.only(top: AppValues.kPadding * 3),
                  child: Column(
                    children: [
                      SizedBox(
                        height: windowHeight * .5,
                        child: ClipRRect(
                          borderRadius:
                              BorderRadius.circular(AppValues.kRadius),
                          child: CachedNetworkImage(
                            imageUrl: widget.url,
                            fit: BoxFit.cover,
                          ),
                        ),
                      ),
                      const Gap(AppValues.kPadding * 2),
                      const CircularProgressIndicator(),
                      const Gap(AppValues.kPadding / 2),
                      AutoSizeText(
                        t.toolsView.studying,
                        style: textTheme.titleLarge!
                            .copyWith(fontWeight: FontWeight.w700),
                      ),
                      const Gap(AppValues.kPadding / 2),
                      AutoSizeText(
                        t.toolsView.wait,
                        style: textTheme.titleMedium!
                            .copyWith(color: AppColors.kOutlineColor),
                      ),
                    ],
                  ),
                );
              },
            ),
          );
  }
}
