import 'package:cached_network_image/cached_network_image.dart';
import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:shimmer/shimmer.dart';
import 'package:x_pictures/src/data.dart';

class GenerationResult extends StatelessWidget {
  const GenerationResult({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(t.generateView.title),
      ),
      body: AppBody(builder: (windowWidth, windowHeight, windowSize) {
        return SingleChildScrollView(
            padding: HorizontalSpacing.centered(windowWidth),
            child: Padding(
              padding:
                  const EdgeInsets.symmetric(vertical: AppValues.kPadding / 2),
              child: Column(children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(AppValues.kRadius),
                  child: CachedNetworkImage(
                    // TODO change this
                    imageUrl: 'https://s1.1zoom.me/big3/446/375561-svetik.jpg',
                    fit: BoxFit.cover,
                    height: windowHeight * 0.5,
                    width: windowWidth,
                    placeholder: (context, url) {
                      return Shimmer.fromColors(
                          baseColor: AppColors.kSecondaryAdditionallyColor,
                          highlightColor: AppColors.kAdditionalColor,
                          period: const Duration(seconds: 4),
                          direction: ShimmerDirection.ttb,
                          child: Container(
                            decoration: const BoxDecoration(
                              color: Colors.white,
                            ),
                          ));
                    },
                  ),
                ),
                const Gap(AppValues.kPadding),
                Row(
                  children:
                      // TODO change this list to a variable
                      [
                    'https://s1.1zoom.me/big3/446/375561-svetik.jpg',
                    'https://s1.1zoom.me/big3/446/375561-svetik.jpg',
                    'https://s1.1zoom.me/big3/446/375561-svetik.jpg',
                    'https://s1.1zoom.me/big3/446/375561-svetik.jpg'
                  ].mapIndexed((i, e) {
                    return Expanded(
                        child: ResultItem(
                            url: e,
                            windowHeight: windowHeight,
                            needPro: i > 0));
                  }).toList(),
                ),
                const Gap(AppValues.kPadding),
                const DecoratedContentWidget(
                    content:
                        // TODO change this text to a variable
                        'Tropical forest with a path in the middle, Far ahead you can see a high mountain, ((On the side of the road there is an old hut)), realistic ambient occlusion, ray tracing lighting, bloom in the sky, high detailed'),
                const Gap(AppValues.kPadding),
                const ResultViewBottomButtons(),
              ]),
            ));
      }),
    );
  }
}
