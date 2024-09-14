import 'package:cached_network_image/cached_network_image.dart';
import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:shimmer/shimmer.dart';
import 'package:x_pictures/src/data.dart';

class GenerationResult extends StatelessWidget {
  final MediaModel? model;
  final GenerateResponse? response;
  const GenerationResult({super.key, this.model, this.response});

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return Scaffold(
      appBar: AppBar(
        leading: const CustomBackButton(),
        title: Text(
          model == null ? t.generateView.title : t.generateView.type.video,
          style: textTheme.bodyMedium!.copyWith(
            fontWeight: FontWeight.w700,
            fontSize: 17,
          ),
        ),
      ),
      body: AppBody(
          builder: (windowWidth, windowHeight, windowSize) =>
              SingleChildScrollView(
                  padding: HorizontalSpacing.centered(windowWidth),
                  child: Padding(
                    padding: EdgeInsets.symmetric(
                      vertical: 14.h,
                    ),
                    child: Column(children: [
                      Padding(
                        padding: EdgeInsets.symmetric(horizontal: 20.h),
                        child: ClipRRect(
                          borderRadius:
                              BorderRadius.circular(AppValues.kRadius),
                          child: CachedNetworkImage(
                            // TODO change this
                            imageUrl:
                                'https://s1.1zoom.me/big3/446/375561-svetik.jpg',
                            fit: BoxFit.cover,
                            height: 400.r,
                            width: windowWidth,
                            placeholder: (context, url) {
                              return Shimmer.fromColors(
                                  baseColor:
                                      AppColors.kSecondaryAdditionallyColor,
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
                      ),
                      Gap(14.h),
                      if (model == null)
                        Padding(
                          padding: EdgeInsets.symmetric(horizontal: 20.h),
                          child: Row(
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
                        ),
                      Gap(20.h),
                      const DecoratedContentWidget(
                          content:
                              // TODO change this text to a variable
                              'Tropical forest with a path in the middle, Far ahead you can see a high mountain, ((On the side of the road there is an old hut)), realistic ambient occlusion, ray tracing lighting, bloom in the sky, high detailed'),
                      Gap(20.h),
                      ResultViewBottomButtons(
                        model: model,
                      ),
                      Gap(20.h),
                    ]),
                  ))),
    );
  }
}
