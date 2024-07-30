import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/core/constant/images.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:percent_indicator/percent_indicator.dart';

class MasterpieceView extends StatefulWidget {
  final PacksStore store;
  final LoraModel model;
  const MasterpieceView({super.key, required this.store, required this.model});

  @override
  State<MasterpieceView> createState() => _MasterpieceViewState();
}

class _MasterpieceViewState extends State<MasterpieceView> {
  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return ChangeNotifierProvider(
      create: (context) => TimeIndicator(),
      child: Scaffold(
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
                  Text(
                    t.masterpiece.title,
                    style: AppStyles.head1TextStyle.copyWith(
                      fontSize: 12.sp,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(
                    height: 10.h,
                  ),
                  Consumer<TimeIndicator>(
                      builder: (context, consumerValue, child) {
                    consumerValue.startTimer(widget.store, widget.model);
                    if (consumerValue.getCurrentTimeRemained == 0) {}
                    return CircularPercentIndicator(
                      radius: 70.r,
                      animation: true,
                      animationDuration: 800,
                      animateFromLastPercent: true,
                      percent: consumerValue.currentPercent,
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
                            '${consumerValue.getCurrentTimeRemained} min',
                            style: AppStyles.head1TextStyle
                                .copyWith(fontSize: 18.sp),
                          )
                        ],
                      ),
                    );
                  }),
                  SizedBox(
                    height: 30.h,
                  ),
                  Text(
                    t.masterpiece.description,
                    style: textTheme.bodyMedium!.copyWith(fontSize: 10.sp),
                    textAlign: TextAlign.center,
                  )
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
