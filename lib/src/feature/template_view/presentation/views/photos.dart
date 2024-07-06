import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/core/constant/icons.dart';
import 'package:x_pictures/src/core/constant/images.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class PhotosView extends StatefulWidget {
  const PhotosView({super.key});

  @override
  State<PhotosView> createState() => _PhotosViewState();
}

class _PhotosViewState extends State<PhotosView> {

  Future<void> _showCustomDialog() async {
    return showDialog<void>(
      context: context,
      barrierDismissible: true,
      builder: (BuildContext context) {
        return SizedBox(
          height: MediaQuery.of(context).size.height * 0.6,
          child: AlertDialog(
            contentPadding: EdgeInsets.zero,
            backgroundColor: Colors.transparent,
            insetPadding: EdgeInsets.zero,
            content: Builder(
              builder: (context) {
                return Padding(
                  padding: const EdgeInsets.all(AppValues.kPadding),
                  child: Container(
                    width: MediaQuery.of(context).size.width,
                    height: MediaQuery.of(context).size.height * 0.5,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(AppValues.kRadius),
                      image: DecorationImage(
                          image: AssetImage(AppImages.monro),
                          alignment: FractionalOffset.topCenter,
                          fit: BoxFit.fitWidth
                      ),
                    ),
                  ),
                );
              },
            ),
            actions: [
              SizedBox(
                width: 250.w,
                height: 50.h,
                child: ElevatedButton.icon(
                  style: ButtonStyle(
                    backgroundColor: WidgetStateProperty.all(Colors.white),
                    shape: WidgetStateProperty.all<RoundedRectangleBorder>(
                     RoundedRectangleBorder(
                       borderRadius: BorderRadius.circular(AppValues.kRadius)
                     ) 
                    )
                  ),
                  onPressed: () {},
                  icon: SvgPicture.asset(AppIcons.download,
                  color: AppColors.kAdditionalColor,
                  width: 20.h,
                  height: 20.h,),
                  label: const Text('Save', style: TextStyle(color: AppColors.kAdditionalColor,
                  fontWeight: FontWeight.bold),),
                ),
              ),
              Container(
                decoration: BoxDecoration(
                  color: AppColors.kAdditionalColor,
                  borderRadius: BorderRadius.circular(AppValues.kRadius)
                ),
                width: 50.h,
                height: 50.h,
                child: IconButton(
                  onPressed: () {},
                  icon: SvgPicture.asset(AppIcons.download,
                  width: 20.h,
                  height: 20.h,
                  color: Colors.white,),
                )
              )
            ],

          ),
        );
      }
    );
  }

  @override
  Widget build(BuildContext context) {
    var size = MediaQuery.of(context).size;

    /*24 is for notification bar on Android*/
    final double itemHeight = (size.height - kToolbarHeight - 24) / 2.5;
    final double itemWidth = size.width / 2;

    return Scaffold(
      appBar: AppBar(
        leading: const CustomBackButton(),
        title: Text('Office'),
        actions: <Widget>[
          TextButton(onPressed: () {},
              child: Text('Save All', style: TextStyle(color: Colors.white),))
        ],
      ),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 15.h),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Ready',
            style: AppStyles.subTitleTextStyle.copyWith(
              fontSize: 10.sp,
            ),),
            SizedBox(
              height: 5.h,
            ),
            Text(
              'Your photos is ready',
              style: AppStyles.head1TextStyle,
            ),
            SizedBox(
              height: 5.h,
            ),
            Text(
              'They will be stored in your personal account',
              style: AppStyles.subTitleTextStyle.copyWith(
                fontSize: 17.sp,
              ),
            ),
            SizedBox(
              height: 10.h,
            ),
            SizedBox(
              height: MediaQuery.of(context).size.height / 1.5,
              child: GridView.count(
                physics: const ScrollPhysics(),
                scrollDirection: Axis.vertical,
                shrinkWrap: true,
                crossAxisSpacing: 6,
                mainAxisSpacing: 6,
                crossAxisCount: 3,
                childAspectRatio: (itemWidth / itemHeight),
                children: List.generate(11, (index) {
                  return Container(
                    decoration: BoxDecoration(
                      image: DecorationImage(
                        image: AssetImage(AppImages.monro),
                        fit: BoxFit.fill
                      ),
                    ),
                    child: Align(
                      alignment: Alignment(0.9, -0.9),
                      child: Container(
                        width: 20.h,
                        height: 20.h,
                        child: IconButton(
                          padding: EdgeInsets.zero,
                          onPressed: () {
                            _showCustomDialog();
                          },
                          icon: SvgPicture.asset(AppIcons.downloadGreyCircle,
                          width: 16.h,
                          height: 16.h,),
                        ),
                      ),
                    ),
                  );
                }),
              ),
            )
          ],
        ),
      ),
    );
  }
}
