import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:percent_indicator/circular_percent_indicator.dart';
import 'package:x_pictures/src/core/constant/images.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';

class MasterpieceBody extends StatefulWidget {
  final PhotosLoaderStore store;
  const MasterpieceBody({super.key, required this.store});

  @override
  State<MasterpieceBody> createState() => _MasterpieceBodyState();
}

class _MasterpieceBodyState extends State<MasterpieceBody> {
  @override
  void initState() {
    widget.store.startTimer();
    super.initState();
  }

  @override
  void dispose() {
    widget.store.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return Scaffold(
      /*appBar: AppBar(
            leading: const CustomBackButton(),
          ),*/
      body: Padding(
        padding: const EdgeInsets.all(AppValues.kPadding),
        child: Container(
          decoration: BoxDecoration(
              image: const DecorationImage(
                  image: AssetImage(
                    AppImages.bannerNoSign,
                  ),
                  fit: BoxFit.cover),
              borderRadius: BorderRadius.circular(AppValues.kRadius)),
          child: SizedBox(
            width: MediaQuery.of(context).size.width,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                AutoSizeText(
                  t.masterpiece.title,
                  style: AppStyles.head1TextStyle.copyWith(
                    fontSize: 17.sp,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(
                  height: 50.h,
                ),
                Observer(builder: (context) {
                  return CircularPercentIndicator(
                      radius: 100.h,
                      animation: true,
                      animationDuration: 800,
                      animateFromLastPercent: true,
                      percent: widget.store.percent,
                      lineWidth: 7.r,
                      circularStrokeCap: CircularStrokeCap.round,
                      backgroundColor: const Color(0xff3B3B5A),
                      progressColor: Colors.orange[900],
                      center: Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          AutoSizeText(
                            '${t.masterpiece.remained}:',
                            style: textTheme.bodyLarge!.copyWith(
                                fontSize: 8.sp, color: AppColors.kOutlineColor),
                          ),
                          AutoSizeText(
                            '${widget.store.seconds} min',
                            style: AppStyles.head1TextStyle
                                .copyWith(fontSize: 18.sp),
                          )
                        ],
                      ));
                }),
                SizedBox(
                  height: 60.h,
                ),
                AutoSizeText(
                  t.masterpiece.description,
                  style: textTheme.bodyMedium!.copyWith(fontSize: 12.sp),
                  textAlign: TextAlign.center,
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}
